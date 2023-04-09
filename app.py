from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from forms import login_form, registration_form, account_form, generator_form
from forms.registration_form import RegistrationForm as registerForm
from forms.login_form import LoginForm as loginForm
from forms.account_form import AccountForm as accountForm
from forms.generator_form import GeneratorForm as generatorForm
from models.User import User
from models.Account import Account
from data_access import user_db, acount_db
from utils import random_generator, authentication, encryption


# NOTE: run the app with flask run

app = Flask(__name__)
# define flask environment variables
app.config['FLASK_ENV'] = 'development'
app.config['FLASK_APP'] = 'app.py'
# TODO: add secret_genrator to random_generator utility with import secrets secrets.token_hex(16)
# set secret key to none until user is logged in
app.config['SECRET_KEY'] = b"secret_key"
# allow access to global variables
global current_user
global accounts
global dev_env
usrID = ''
accounts = []
account = {""}
# set dev, remove when done
dev_env = True

test_data = {"key_1": "value_1", "key_2": "value_2", "key_3": "value_3", "key_4": "value_4", "key_5": "value_5"}

# current_user should be user object; set on login or register
current_user = None

# create user save usr to db then redirect to home
@app.route('/register/', methods=['GET', 'POST'])
def register():
    # allow access to global variables
    global current_user
    global accounts
    global dev_env
    form = registerForm()
    # validation occurs on form submission
    if form.validate_on_submit():
        # EqaulTo validator validates passwords match dont need to add the logic
        try:
            # get user info to register new user
            username = form.username.data
            email = form.email.data
            password = form.password.data
            # initialize new user object
            current_user = User(username, email)
            # set user info and encrypt password
            current_user.set_salt()
            current_user.set_password(password)
            current_user.set_key()
            current_user.set_user_id()
            # save user to database
            successful_insert = user_db.insert_user(current_user)
            # if successful, log user in, send success message, and set secret key to user's key
            if successful_insert:
                flash("Logged in successfully!")
                app.config['SECRET_KEY'] = current_user.get_key()
                # redirect to home page pass through entire current_user object
                return redirect(url_for('home', current_user=current_user, username = current_user.username))
            else:
                flash("Failed to register user!", category="error")
                return render_template('register.html', form=form)
        except Exception as err:
            flash("Failed to register user!", category="error")
            print(err)
    else:
        return render_template('register.html', form=form)


@app.route('/', methods=['GET', 'POST'])
def login():
    # allow access to global variables
    global current_user
    global accounts
    global dev_env
    # change to jwt authentication
    form = loginForm()
    if form.validate_on_submit():
        username = form.username.data
        plain_text_password = form.password.data
        # NOTE flash message goes from server to client, can show success/error with them. Not sure what these flashes do.
        # flash will output values somewhere im not sure where
        # %s might need changed
        #flash('username: %s' % form.username.data)
        #flash('plaintext pw: %s' % form.password.data)
        # lookup username, return salt; if no user found return error
        salt = user_db.fetch_user_salt(username)
        if salt is None:
            flash("Could not find user %s" % username)
        else:
            #if user found, use salt to encrypt entered password
            encryption.encrypt_password(plain_text_password, salt)
        # check to see if user's entered password is correct
        is_match = authentication.verify_password(username, plain_text_password)
        # if password is correct, log user in
        if is_match:
            accountform = accountForm()
            # fetch user info from database
            user_info = user_db.fetch_user(username)
            # initialize user object using user info from database
            current_user = User(username, user_info['email'])
            current_user.salt = user_info['salt']
            current_user.user_id = user_info['user_id']
            current_user.set_key(plain_text_password)
            # set secret key to user's key
            app.config['SECRET_KEY'] = current_user.get_key()
            # send success message to user
            flash("Logged in successfully!")
            # redirect to management page sending through entire current_user object
            return redirect(url_for('manage', current_user=current_user, username = current_user.username, form=accountform))
        # on failed login, send error message, return to login page
        else:
            flash("Failed to login!", category="error")
            return render_template('login_html', form=form)
    # on failed login, send error message, return to login page
    else:
        flash("Failed to login!", category="error")
        return render_template('login.html', form=form)


@app.route('/manage/<username>', methods=['GET', 'POST'])
def manage(username):
    global current_user
    global accounts
    global dev_env
    form = accountForm()
    if not dev_env:
        # get list of currentUsr's accounts
        accounts = acount_db.fetch_user_accounts(current_user.usr_id, username)
    else:
         # create dev_user, add account; remove when done with development
         current_user = User("dev_user", "hzdkv@example.com")
         current_user.user_id = "0"
         account = Account('00000aaa', 0, 'gmail', 'zdev1@example.com', 'plainTxt')
         accounts.append(account)
    return render_template('manage.html', current_user=current_user, username = current_user.username, form=form, test_data=test_data)


@app.route('/generator/<username>', methods=['GET', 'POST'])
def generator(username):
    global current_user
    global accounts
    global dev_env
    if dev_env is True:
        current_user = User("dev_user", "hzdkv@example.com")
    form = generatorForm()
    if form.validate_on_submit():
        # get password criteria from user
        password_length = form.password_length.data
        letter_count = form.letter_count.data
        number_count = form.letter_count.data
        symbol_count = form.symbol_count.data
        # generate password with criteria
        generated_password = random_generator.generate_pwd(
            password_length,
            letter_count,
            number_count,
            symbol_count
        )
        # set password form to show generated password
        form.generated_password.data = generated_password
        # check is useless if all cases return same redirect
        if generated_password is not None:
            return render_template('generator.html', current_user=current_user, form=form, username = current_user.username)
        else:
            return render_template('generator.html', current_user=current_user, form=form, username = current_user.username)
    return render_template('generator.html', current_user=current_user, username=current_user.username, form=form)


# example for updating dictionary value (see manage.html for context)
@app.route('/update', methods=['POST'])
def update():
    global current_user
    global accounts
    global dev_env
    updated_data = request.get_json()
    key = updated_data.get('key')
    value = updated_data.get('value')

    if key in test_data:
        test_data[key] = value
        return jsonify({'status': 'success', 'message': f'Updated {key} to {value}'}), 200
    else:
        return jsonify({'status': 'error','message': f'Key {key} not found'}), 400
    


# use this so we can just run "python app.py" in terminal
app.run(debug=True)