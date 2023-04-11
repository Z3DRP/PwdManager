from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from forms import login_form, registration_form, account_form, generator_form
from forms.registration_form import RegistrationForm as registerForm
from forms.login_form import LoginForm as loginForm
from forms.account_form import AccountForm as accountForm
from forms.generator_form import GeneratorForm as generatorForm
from models.User import User
from models.Account import Account
from data_access import user_db, acount_db
from utils import random_generator

# TODO when opening the app again set these environment variables so server doesnt have to be restarted after each change
# export FLASK_ENV=development && export FLASK_APP=app.py
# run with
# flask run

app = Flask(__name__)
# define flask environment variables
app.config['FLASK_ENV'] = 'development'
app.config['FLASK_APP'] = 'app.py'
# TODO: add secret_genrator to random_generator utility with import secrets secrets.token_hex(16)
app.config['SECRET_KEY'] = 'something for not eventually make byte string maybe'
usrID = ''
accounts = []
account = {""}
#currentUsr should be a user object
currentUsr = None
# set dev, remove when done
dev_env = True
#create dev_user, add account; remove when done with development
if dev_env:
         currentUsr = User("dev_user", "hzdkv@example.com")
         currentUsr.userID = "0"
         account1 = Account('00000aaa', 0, 'gmail', 'gmailUsername', 'zdev1@example.com', 'plainTxt')
         accounts.append(account1)
         account2 = Account('00000bbb', 0, 'github', 'githubUsername', 'email2@mail.com', 'githubPassword')
         accounts.append(account2)


# create user save usr to db then redirect to home
@app.route('/register/', methods=['GET', 'POST'])
def register():
    # allow access to global variables
    global currentUsr
    global accounts
    global dev_env
    # create user save usr to db then redirect to home
    form = registerForm()
    # validation occurs on form submission
    if form.validate_on_submit():
        # EqaulTo validator validates passwords match dont need to add the logic
        try:
            # get user info to register new user
            usrname = form.username.data
            email = form.email.data
            pwd = form.password.data
            # initialize new user object
            currentUsr = User(usrname, email)
            # set user info
            currentUsr.set_password(pwd)
            # save user to database
            successful_insert = user_db.insert_user(currentUsr)
            if successful_insert:
                # redirect to home page pass through entire currentUsr object
                return redirect(url_for('home', currentUsr=currentUsr, usrname = currentUsr.usrname))
            else:
                # need to show error if insert failed
                return render_template('register.html', form=form)
        except Exception as err:
            # figure out way to display error and success to usr
            print(err)
    else:
        return render_template('register.html', form=form)


@app.route('/', methods=['GET', 'POST'])
def login():
    # allow access to global variables
    global currentUsr
    global accounts
    global dev_env
    # change to jwt authentication
    form = loginForm()
    test_err_msg = 'test error message'
    if form.validate_on_submit():
        usrname = form.username.data
        pwd = form.password.data
        # NOTE flash message goes from server to client, can show success/error with them. Not sure what these flashes do.
        # flash will output values somewhere im not sure where
        # %s might need changed
        flash('username: %s' % form.username.data)
        flash('plaintext pw: %s' % form.password.data)
        isMatch = User.verify_password(usrname, pwd)
        # if password is correct, log user in
        if isMatch:
            accountform = accountForm()
            # fetch user info from database
            user_info = user_db.fetch_user(usrname)
            # initialize user object using user info from database
            current_user = User(usrname, user_info['email'])
            current_user.user_id = user_info['user_id']
            # TODO: login success message display
            # redirect to management page sending through entire currentUsr object
            return redirect(url_for('manage', currentUsr=currentUsr, usrname = currentUsr.usrname, form=accountform))
        # on failed login, send error message, return to login page
        else:
            return render_template('login_html', form=form, emsg=test_err_msg)
    # on failed login, send error message, return to login page
    else:
        return render_template('login.html', form=form, emsg=test_err_msg)


@app.route('/manage/<usrname>', methods=['GET', 'POST'])
def manage(usrname):
    global currentUsr
    global accounts
    global dev_env
    form = accountForm()
    if not dev_env:
        # get list of currentUsr's accounts
        accounts = acount_db.fetch_user_accounts(currentUsr.usr_id, usrname)
    # returns to manage page, passes through currentUsr object, usrname and the user's accoutns
    return render_template('manage.html', currentUsr=currentUsr, usrname = currentUsr.usrname, form=form, accounts=accounts)


@app.route('/generator/<usrname>', methods=['GET', 'POST'])
def generator(usrname):
    global currentUsr
    global accounts
    global dev_env
    #if dev_env is True:
    #    current_user = User("dev_user", "hzdkv@example.com")
    form = generatorForm()
    if form.validate_on_submit():
        # get password criteria from user
        pwd_length = form.pwd_length.data
        letter_count = form.letter_count.data
        number_count = form.number_count.data
        symbol_count = form.symbol_count.data
        # generate password with criteria
        gen_pwd = random_generator.generate_pwd(
            pwd_length,
            letter_count,
            number_count,
            symbol_count
        )
        # set password form to show generated password
        form.generated_pwd.data = gen_pwd
        # check is useless if all cases return same redirect
        if gen_pwd is not None:
            return render_template('generator.html', currentUsr=currentUsr, form=form, usrname = currentUsr.usrname)
        else:
            return render_template('generator.html', currentUsr=currentUsr, form=form, usrname = currentUsr.usrname)
    return render_template('generator.html', currentUsr=currentUsr, form=form, usrname = currentUsr.usrname)
