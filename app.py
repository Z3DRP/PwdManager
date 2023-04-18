from flask import Flask, render_template, redirect, url_for, request, session
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

@app.route('/register/', methods=['GET', 'POST'])
def register():
    # create user save usr to db then redirect to home
    form = registerForm()
    toast_data = {}
    if request.method == 'POST':
        # validate form will happen after submit/register
        if form.validate_on_submit():
            # EqaulTo validator validates passwords match dont need to add the logic
            try:
                usrname = form.username.data
                email = form.email.data
                pwd = form.pwd.data
                user = User(True, usrname, email, pwd)
                successful_insert = user_db.insert_user(user)
                if successful_insert.get('wasSuccess'):
                    session['user'] = json.dumps(user)
                    session['username'] = usrname
                    session['userId'] = user.userId
                    # test how converting python's True/False to js true false works
                    # toast_data['wasSuccess'] = successful_insert.get('wasSuccess')
                    toast_data['wasSuccess'] = 1
                    toast_data['successMessage'] = successful_insert.get('message')
                    accountform = accountForm()
                    return redirect(url_for('manage', toastData=toast_data, form=accountform))
                else:
                    # toast_data['wasSuccess'] = successful_insert.get('wasSuccess')
                    toast_data['wasSuccess'] = 0
                    toast_data['errorMessage'] = successful_insert.get('message')
                    return render_template('register.html', toastData=toast_data, form=form)
            except Exception as err:
                print(err)
    else:
        toast_data['initialLoad'] = 1
        return render_template('register.html', toastData=toast_data, form=form)


@app.route('/', methods=['GET', 'POST'])
def login():
    # TODO add cacheing
    # TODO change to jwt authentication
    form = loginForm()
    test_err_msg = None
    toast_data = {}
    test_success_msg = 'update success'
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                usrname = form.username.data
                pwd = form.pwd.data
                usr_auth = User.verify_password(usrname, pwd)
                if usr_auth.get('isMatch'):
                    currentUsr = User.authenticated_user(usrname, usr_auth['email'], usr_auth['userid'])
                    # store usr obj in session as json or just values separate
                    session['user'] = json.dumps(currentUsr)
                    session['username'] = usrname
                    session['userId'] = currentUsr['userId']
                    toast_data['successMessage'] = 'login successful'
                    toast_data['wasSuccess'] = usr_auth.get('isMatch')
                    accountform = accountForm()
                    # look at creating custom url converters bc might not be able to pass in dict to manage for url
                    return redirect(url_for('manage', form=accountform))
                # might be redundant
                else:
                    toast_data['errorMessage'] = 'login failed'
                    toast_data['wasSuccess'] = 0
                    return render_template('login_html', form=form, toastData=json.dumps(toast_data))
            except Exception as err:
                # need to make a error page send error to
                print(err)
    else:
        toast_data['initialLoad'] = 1
        # toast_data['errorMessage'] = 'login failed'
        # toast_data['wasSuccess'] = 0
        return render_template('login.html', form=form, toastData=json.dumps(toast_data))


@app.route('/manage/<username>', methods=['GET', 'POST'])
def manage(username):
    toast_data = {}
    # get accounts then create list of all accounts
    accountform = accountForm()
    accounts = []
    if request.method == 'GET':
        if not session.get('username'):
            toast_data['initialLoad'] = 1
            loginform = loginForm()
            return redirect(url_for('login.html', form=loginform, toastData=json.dumps(toast_data)))
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
                print(err)
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
                    # add new account to list then store in session so it will be retrieved during next get method
                    accounts.append(newAccount)
                    # this will need to be changed to cacheing due to session storage limits
                    # serialize account list and store in session this helps prevent unnecessary database calls
                    session['accounts'] = json.dumps(accounts)
                    newForm = accountForm()
                    # toast_data['wasSuccess'] = result.get('wasSuccess')
                    toast_data['wasSuccess'] = 1
                    toast_data['successMessage'] = result.get('message')
                    return redirect(url_for('manage', toastData=toast_data, form=newForm))
                else:
                    newForm = accountForm()
                    # toast_data['wasSuccess'] = result.get('wasSuccess')
                    toast_data['wasSuccess'] = 0
                    toast_data['successMessage'] = result.get('message')
                    return redirect(url_for('manage', toastData=toast_data, form=newForm))
            except Exception as err:
                # could also display on error page
                toast_data['wasSuccess'] = 0
                toast_data['errorMessage'] = err
                return redirect(url_for('manage', toastData=toast_data, form=accountform))
    else:
        return render_template(url_for('manage', toastData=toast_data, form=accountform))

@app.route('/generator/', methods=['GET', 'POST'])
def generator():
    pwdGenerated = False
    toast_data = {}
    form = generatorForm()
    if request.method == 'POST':
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
                form.generated_pwd.data = gen_pwd
                if gen_pwd is not None:
                    pwdGenerated = True
                    return render_template('generator.html', form=form)
                else:
                    pwdGenerated = False
                    return render_template('generator.html', form=form)
            return render_template('generator.html', form=form)
        else:
            loginform = loginForm()
            return redirect(url_for('login', toastData=toast_data, form=loginform))
    else:
        return render_template(url_for('generator', form=form))


@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('username', None)
    session.pop('userId', None)
    session.pop('accounts', None)
    toast_data = {'initialLoad': 1}
    loginform = loginForm()
    return redirect(url_for('login', toastData=toast_data, form=loginform))
