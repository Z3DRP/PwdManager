from flask import Flask, render_template, redirect, url_for, request, session, flash
from forms.registration_form import RegistrationForm as registerForm
from forms.login_form import LoginForm as loginForm
from forms.account_form import AccountForm as accountForm
from forms.generator_form import GeneratorForm as generatorForm
from models.User import User
from models.Account import Account
from data_access import user_db, account_db
from utils import random_generator
from utils.Secret import get_secret
from flask_session import Session
from validator.Validator import validateLogin
import json

# TODO when opening the app again set these environment variables so server doesnt have to be restarted after each change
# export FLASK_ENV=development
# export FLASK_APP=app.py
# run with
# flask run

app = Flask(__name__)
# should be moved out
# could mak another file that generates a random secrect with import secrets secrets.token_hex(16)
app.config['SECRET_KEY'] = get_secret()
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


@app.route('/register', methods=['GET', 'POST'])
def register():
    # create user save usr to db then redirect to home
    form = registerForm()
    toast_data = {}
    if form.validate_on_submit():
        # EqaulTo validator validates passwords match dont need to add the logic
        try:
            usrname = form.username.data
            email = form.email.data
            pwd = form.password.data
            user = User(True, usrname, email, pwd)
            successful_insert = user_db.insert_user(user)
            if successful_insert.get('wasSuccess'):
                # temporarily use flash instead of toasts
                flash(f'Account created for {usrname}', 'success')
                session['user'] = json.dumps(user)
                session['username'] = usrname
                session['userId'] = user.userId
                # test how converting python's True/False to js true false works
                # toast_data['wasSuccess'] = successful_insert.get('wasSuccess')
                toast_data['wasSuccess'] = 1
                toast_data['successMessage'] = successful_insert.get('message')
                return redirect(url_for('manage'))
            else:
                # toast_data['wasSuccess'] = successful_insert.get('wasSuccess')
                flash(f'A error occurred while trying to create account for {usrname}')
                toast_data['wasSuccess'] = 0
                toast_data['errorMessage'] = successful_insert.get('message')
        except Exception as err:
            print(err)
    return render_template('register.html', toastData=toast_data, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # TODO add cacheing
    # TODO change to jwt authentication
    form = loginForm()
    toast_data = {}
    test_success_msg = 'update success'
    if form.validate_on_submit():
        try:
            usrname = form.username.data
            pwd = form.password.data
            usr = User.setUserLogin(usrname, pwd)
            usr_auth = usr.verify_password(usrname, pwd)
            if usr_auth.get('isMatch'):
                currentUsr = User.authenticated_user(usrname, usr_auth['email'], usr_auth['userid'])
                # store usr obj in session as json or just values separate
                session['user'] = json.dumps(currentUsr)
                session['username'] = usrname
                session['userId'] = currentUsr['userId']
                toast_data['successMessage'] = 'login successful'
                toast_data['wasSuccess'] = usr_auth.get('isMatch')
                # look at creating custom url converters bc might not be able to pass in dict to manage for url
                return redirect(url_for('manage'))
            else:
                # temp messages with flash instead of toast
                flash('Login failed please check username and password', 'danger')
                toast_data['errorMessage'] = 'login failed'
                toast_data['wasSuccess'] = usr_auth.get('isMatch')
                # dont need to return here because it will fall through to bottom return
        except Exception as err:
            # exceptions might need an error page
            flash(f'{err}', 'danger')
    return render_template('login.html', form=form, toastData=json.dumps(toast_data))


@app.route('/manage/<username>', methods=['GET', 'POST'])
def manage(username):
    toast_data = {}
    # get accounts then create list of all accounts
    accountform = accountForm()
    accounts = []
    if request.method == 'GET':
        if not session.get('username'):
            toast_data['message'] = None
            loginform = loginForm()
            return redirect(url_for('login'))
        else:
            try:
                # if usr has been logged in and accounts were stored during a insert or updated
                if session.get('accounts'):
                    # deserialize list of accounts
                    accounts = json.loads(session.get('accounts'))
                # if no account are in current session fetch them
                else:
                    # deserialize user obj and fetch accounts
                    currentUsr = json.loads(session.get('user'))
                    # TODO create refactor fetch urs accounts to return dict
                    accounts = account_db.fetch_user_accounts(currentUsr)
                # create a default account so there is at least one account card or a blank card
                defaultAccount = Account.createDefaultAccount(session.get('userId'))
                accounts.append(defaultAccount)
                # using session data we will not have to pass in username
                return render_template(url_for('manage.html', toastData=toast_data, form=accountform))
            except Exception as err:
                # TODO send values from dict returned from fetch usr accounts to toast
                flash(f'{err},' 'danger')
    # we will need more logic more than likely in js
    # need to grab the account id of the card whose 'create/edit' button was clicked
    # then pass that from js to python to select that account from account list
    # we will need to handle create and edit differently
    if request.method == 'POST':
        if accountform.validate_on_submit():
            try:
                # note user id does not come from form bc it is for internal use
                usrId = session.get('userId')
                name = accountform.account_name.data
                usrname = accountform.username.data
                email = accountform.email.data
                pwd = accountform.pwd.data
                newAccount = Account(name, usrId, usrname, email, pwd)
                # TODO create insert account method that returns dict like 'update_account && insert_user' methods
                result = account_db.insert_account(newAccount)
                if result.get('wasSuccess'):
                    flash(f'{result.get("message")}', 'success')
                    # add new account to list then store in session, so it will be retrieved during next get method
                    accounts.append(newAccount)
                    # this will need to be changed to cacheing due to session storage limits
                    # serialize account list and store in session this helps prevent unnecessary database calls
                    session['accounts'] = json.dumps(accounts)
                    newForm = accountForm()
                    # toast_data['wasSuccess'] = result.get('wasSuccess')
                    toast_data['wasSuccess'] = 1
                    toast_data['successMessage'] = result.get('message')
                    # might not have to be redirect might need something else to re-render page with new accounts
                    return redirect(url_for('manage'))
                else:
                    # newForm = accountForm()
                    flash(f'{result.get("message")}', 'danger')
                    # toast_data['wasSuccess'] = result.get('wasSuccess')
                    toast_data['wasSuccess'] = 0
                    toast_data['successMessage'] = result.get('message')
                    # return redirect(url_for('manage', toastData=toast_data, form=newForm))
            except Exception as err:
                # could also display on error page
                flash(f'{err}', 'danger')
                toast_data['wasSuccess'] = 0
                toast_data['errorMessage'] = err
                return redirect(url_for('manage'))
    else:
        return render_template(url_for('manage'))

@app.route('/generator', methods=['GET', 'POST'])
def generator():
    pwdGenerated = False
    toast_data = {}
    form = generatorForm()
    if session.get('username'):
        if form.validate_on_submit():
            pwd_len = form.pwd_length.data
            letter_count = form.letter_count.data
            number_count = form.letter_count.data
            symbol_count = form.symbol_count.data
            # extra_fields = form.extra_fields.data
            gen_pwd = random_generator.generate_pwd(
                pwd_len,
                letter_count,
                number_count,
                symbol_count
            )
            return render_template('generator.html', form=form, password=gen_pwd)
    else:
        loginform = loginForm()
        return redirect(url_for('login'))
    return render_template(url_for('generator', form=form))


@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('username', None)
    session.pop('userId', None)
    session.pop('accounts', None)
    toast_data = {'message': None}
    loginform = loginForm()
    return redirect(url_for('login', toastData=toast_data, form=loginform))


if __name__ == '__main__':
    app.run(debug=True)
