from flask import Flask, render_template, redirect, url_for, request, session
from forms.registration_form import RegistrationForm as registerForm
from forms.login_form import LoginForm as loginForm
from forms.account_form import AccountForm as accountForm
from forms.generator_form import GeneratorForm as generatorForm
from models.User import User
from models.Account import Account
from data_access import user_db, acount_db
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
usrID = ''
accounts = []
account = {""}
currentUsr = None


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
                    toast_data['wasSuccess'] = successful_insert.get('wasSuccess')
                    toast_data['successMessage'] = successful_insert.get('message')
                    return redirect(url_for('home', usr=user))
                else:
                    toast_data['wasSuccess'] = successful_insert.get('wasSuccess')
                    toast_data['successMessage'] = successful_insert.get('message')
                    return render_template('register.html', form=form)
            except Exception as err:
                print(err)
    else:
        return render_template('register.html', form=form)


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
                    global currentUsr
                    currentUsr = User.authenticated_user(usrname, usr_auth['email'], usr_auth['userid'])
                    # store usr obj in session as json or just values seperate
                    session['user'] = json.dumps(currentUsr)
                    session['username'] = usrname
                    session['userId'] = currentUsr['userId']
                    toast_data['successMessage'] = 'login successful'
                    toast_data['wasSuccess'] = usr_auth.get('isMatch')
                    accountform = accountForm()
                    # look at creating custom url converters bc might not be able to pass in dict to manage for url
                    return redirect(url_for('manage', username=usrname, user=currentUsr, form=accountform))
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
    # get accounts then create list of all accounts
    form = accountForm()
    accounts = []
    # TODO remove this after dev done
    if not session.get('username'):
        dev_env = True
        if not dev_env:
            accounts = acount_db.fetch_user_accounts(session['username'])
            # depending on length of account put in session but cacheing would be better
        else:
            usr_id = 0
            # make a default account so atleast one card is dispalyed
            usrAccount = Account('0000000', 0, 'gmail', 'noAccounts@2xample.com', 'plainTxt')
            accounts.append(account)
        return render_template('manage.html', usrname=username, form=form)
    else:
        return redirect('/')


@app.route('/generator/', methods=['GET', 'POST'])
def generator():
    pwdGenerated = False
    form = generatorForm()
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

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('username', None)
    session.pop('userId', None)
    return redirect(url_for('login'))
