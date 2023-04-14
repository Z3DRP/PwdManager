from flask import Flask, render_template, redirect, url_for, flash
from forms.registration_form import RegistrationForm as registerForm
from forms.login_form import LoginForm as loginForm
from forms.account_form import AccountForm as accountForm
from forms.generator_form import GeneratorForm as generatorForm
from models.User import User
from models.Account import Account
from data_access import user_db, acount_db
from utils import random_generator

# TODO when opening the app again set these environment variables so server doesnt have to be restarted after each change
# export FLASK_ENV=development
# export FLASK_APP=app.py
# run with
# flask run

app = Flask(__name__)
# should be moved out
# could mak another file that generates a random secrect with import secrets secrets.token_hex(16)
app.config['SECRET_KEY'] = 'something for not eventually make byte string maybe'
usrID = ''
accounts = []
account = {""}
currentUsr = None
@app.route('/register/', methods=['GET', 'POST'])
def register():
    # create user save usr to db then redirect to home
    form = registerForm()
    # validate form will happen after submit/register
    if form.validate_on_submit():
        # EqaulTo validator validates passwords match dont need to add the logic
        try:
            usrname = form.username.data
            email = form.email.data
            pwd = form.pwd.data
            # confirmed_pwd = form.confirm_pwd.data
            usr = User(usrname, email)
            usr.set_password(pwd)
            # v2 password set usr.set_password(pwd, True)
            successful_insert = user_db.insert_user(usr)
            if successful_insert:
                return redirect(url_for('home', usrname=usrname))
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
    # change to jwt authentication
    form = loginForm()
    test_err_msg = None
    if form.validate_on_submit():
        usrname = form.username.data
        pwd = form.pwd.data
        # v2 pwd set usr.set_password(pwd, False)

        # flash will output values somewhere im not sure where
        # %s might need changed
        flash('username: %s' % form.username.data)
        flash('plaintext pw: %s' % form.pwd.data)
        isMatch = User.verify_password(usrname, pwd)

        if isMatch:
            hasError = True
            global currentUsr
            currentUsr = usrname
            auth_failed = False
            accountform = accountForm()
            return redirect(url_for('manage', usrname=usrname, form=accountform))
        # might be redundant
        else:
            hasError = False
            auth_failed = True
            return render_template('login_html', form=form, emsg=test_err_msg)
    else:
        hasError = False
        return render_template('login.html', form=form, emsg=test_err_msg)


@app.route('/manage/<usrname>', methods=['GET', 'POST'])
def manage(usrname):
    # get accounts then create list of all accounts
    form = accountForm()
    # TODO remove this after dev done
    dev_env = True
    if not dev_env:
        usr_id = user_db.fetch_user_id(usrname)
        usr_accounts = acount_db.fetch_user_accounts(usr_id, usrname)
    # else:
    #     usr_id = 0
    #     account = Account('00000aaa', 0, 'gmail', 'zdev1@example.com', 'plainTxt')
    #     accounts.append(account)
    return render_template('manage.html', usrname=usrname, form=form)


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
