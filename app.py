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
        try:
            usrname = form.username.data
            email = form.email.data
            pswd = form.password.data
            user = User.set_new_User(usrname, email, pswd)
            # convert to json before passing to db method
            # usr = json.dumps(user.__dict__)
            successful_insert = user_db.insert_user(user.getUserJson())
            if successful_insert.get('wasSuccess'):
                # temporarily use flash instead of toasts
                flash(f'Account created for {usrname}', category='success')
                session['user'] = user.getUserJson()
                session['username'] = usrname
                session['userId'] = user.userId
                toast_data['wasSuccess'] = successful_insert.get('wasSuccess')
                toast_data['successMessage'] = successful_insert.get('message')
                toast_data['hasAlert'] = True
                return redirect(url_for('manage', username=usrname))
            else:
                flash(f'A error occurred while trying to create account for {usrname}', category='danger')
                toast_data['wasSuccess'] = successful_insert.get('wasSuccess')
                toast_data['errorMessage'] = successful_insert.get('message')
                toast_data['hasAlert'] = True
        except Exception as err:
            flash(f'Error:: {err}', category='danger')
    # TODO add more functionality to handle not valid submits
    return render_template('register.html', toastData=toast_data, form=form)


@app.route('/', methods=['GET', 'POST'])
def login():
    # TODO add cacheing
    # TODO change to jwt authentication
    form = loginForm()
    toast_data = {}
    if form.validate_on_submit():
        try:
            usrname = form.username.data
            pwd = form.password.data
            usr = User.set_user_login(usrname, pwd)
            authInfo = usr.verify_password(usrname, pwd)
            if authInfo.get('isMatch'):
                currentUsr = User(authInfo['userId'], usrname, authInfo['email'])
                # store usr obj in session as json or just values separate
                session['user'] = currentUsr.getUserJson()
                session['username'] = usrname
                session['userId'] = currentUsr.get_user_id()
                toast_data['successMessage'] = 'login successful'
                toast_data['wasSuccess'] = authInfo.get('isMatch')
                toast_data['hasAlert'] = True
                # look at creating custom url converters bc might not be able to pass in dict to manage for url
                # return redirect(url_for('manage'))
                return redirect(url_for('manage', username=usrname, toastData=json.dumps(toast_data)))
            else:
                # temp messages with flash instead of toast
                flash('Login failed please check username and password', category='danger')
                toast_data['errorMessage'] = 'login failed'
                toast_data['wasSuccess'] = authInfo.get('isMatch')
                # dont need to return here because it will fall through to bottom return
        except Exception as err:
            # exceptions might need an error page
            flash(f'{err}', category='danger')
    return render_template('login.html', form=form, toastData=json.dumps(toast_data))


@app.route('/manage/<username>/', methods=['GET', 'POST'])
def manage(username):
    SCRIPT_ROOT = json.dumps(request.script_root)
    # TODO we will not be able to use flask forms for the mangement cards
    # we would have to make multiple instances of the flask forms and pass each one to html
    # we have no idea of knowing how many accounts the user has so will not be able to pass each in
    # TODO convert flask forms on mangement page to strictly html forms rewrite this
    #  method to handle request.method == 'POST' && 'GET'
    isLoading=True
    toast_data = {}
    # get accounts then create list of all accounts
    accounts = []
    if session.get('username'):
        try:
            if request.method == 'GET':
                usr = session['user']
                accounts = account_db.fetch_user_accounts(usr)
                # return render_template('manage.html', username=session.get('username'), accounts=accounts, root=SCRIPT_ROOT)
            elif request.method == 'POST':
                pass
        except Exception as err:
            flash(f'{err}', category='danger')
    else:
        return redirect(url_for('login'))
    return render_template('manage.html', username=username, toastData=json.dumps(toast_data), root=SCRIPT_ROOT)
    # if request.method == 'GET':
    #     if not session.get('username'):
    #         toast_data['message'] = None
    #         loginform = loginForm()
    #         return redirect(url_for('login'))
    #
    #     else:
    #         try:
    #             # if usr has been logged in and accounts were stored during a insert or updated
    #             if session.get('accounts'):
    #                 # deserialize list of accounts
    #                 accounts = json.loads(session.get('accounts'))
    #             # if no account are in current session fetch them
    #             else:
    #                 # deserialize user obj and fetch accounts
    #                 currentUsr = json.loads(session.get('user'))
    #                 # TODO create refactor fetch urs accounts to return dict
    #                 accounts = account_db.fetch_user_accounts(currentUsr)
    #             # create a default account so there is at least one account card or a blank card
    #             defaultAccount = Account.createDefaultAccount(session.get('userId'))
    #             accounts.append(defaultAccount)
    #             # using session data we will not have to pass in username
    #             return render_template(url_for('manage.html', username='username', toastData=toast_data, form=accountform))
    #         except Exception as err:
    #             # TODO send values from dict returned from fetch usr accounts to toast
    #             flash(f'{err},' 'danger')
    #     return render_template('manage.html', username='username', toastData=toast_data, form=accountform)
    # # we will need more logic more than likely in js
    # # need to grab the account id of the card whose 'create/edit' button was clicked
    # # then pass that from js to python to select that account from account list
    # # we will need to handle create and edit differently
    # if request.method == 'POST':
    #     if accountform.validate_on_submit():
    #         try:
    #             # note user id does not come from form bc it is for internal use
    #             usrId = session.get('userId')
    #             name = accountform.account_name.data
    #             usrname = accountform.username.data
    #             email = accountform.email.data
    #             pwd = accountform.pwd.data
    #             newAccount = Account(name, usrId, usrname, email, pwd)
    #             # TODO create insert account method that returns dict like 'update_account && insert_user' methods
    #             result = account_db.insert_account(newAccount)
    #             if result.get('wasSuccess'):
    #                 flash(f'{result.get("message")}', 'success')
    #                 # add new account to list then store in session, so it will be retrieved during next get method
    #                 accounts.append(newAccount)
    #                 # this will need to be changed to cacheing due to session storage limits
    #                 # serialize account list and store in session this helps prevent unnecessary database calls
    #                 session['accounts'] = json.dumps(accounts)
    #                 newForm = accountForm()
    #                 toast_data['wasSuccess'] = result.get('wasSuccess')
    #                 toast_data['successMessage'] = result.get('message')
    #                 # might not have to be redirect might need something else to re-render page with new accounts
    #                 return redirect(url_for('manage', username='username'))
    #             else:
    #                 # newForm = accountForm()
    #                 flash(f'{result.get("message")}', 'danger')
    #                 toast_data['wasSuccess'] = result.get('wasSuccess')
    #                 toast_data['successMessage'] = result.get('message')
    #                 # return redirect(url_for('manage', toastData=toast_data, form=newForm))
    #         except Exception as err:
    #             # could also display on error page
    #             flash(f'{err}', 'danger')
    #             toast_data['wasSuccess'] = False
    #             toast_data['errorMessage'] = err
    #             return redirect(url_for('manage', username='username'))
    # else:
    #     return render_template('manage.html', username='username', form=accountform)



@app.route('/update/<accountName>')
def upsert(accountId, userId):
    # create a dict from session id then pass to form to populate fields
    toast_data = {}
    accountform = accountForm()
    if session.get('username'):
        if accountform.validate_on_submit():
            try:
                # TODO add check to see if action is update or create
                name = accountform.account_name.data
                username = accountform.username.data
                email = accountform.email.data
                password = accountform.pwd.data
                account = Account.createNewAccount(name, username, userId, email, password)
                accountJson = account.getAccountJson()
                result = account_db.update_account(accountJson)
                if result.get('wasSuccess'):
                    return redirect(url_for('manage', username=username, toastData=json.dumps(toast_data)))
                else:
                    flash(f'{result.get("message")}', category="danger")
            except Exception as err:
                flash(f'{err}', category="danger")
        else:
            selectedAccount = getSelectedAccount()
            accountform = accountForm(formdata=selectedAccount)
    else:
        return redirect(url_for("login"))


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
    return render_template('generator.html', form=form)


@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('username', None)
    session.pop('userId', None)
    session.pop('accounts', None)
    toast_data = {'message': None}
    loginform = loginForm()
    return redirect(url_for('login', toastData=toast_data, form=loginform))


def toJson(classInstance):
    # to convert python class instance to json must get dict version of class with __dict__
    return json.dumps(classInstance.__dict__)

def getSelectedAccount():
    selectedId = session.get('selectedAccount')
    accounts = json.loads(session.get('accounts'))
    return accounts.get(selectedId)

if __name__ == '__main__':
    app.run(debug=True)
