from flask import Flask, render_template, redirect, url_for, flash
from forms import login_form, registration_form, account_form, generator_form
from models.User import User
from models.Account import Account
from data_access import db
from utils import random_generator

app = Flask(__name__)
# should be moved out
# could mak another file that generates a random secrect with import secrets secrets.token_hex(16)
app.config['SECRET_KEY'] = 'something for not eventually make byte string maybe'
usrID = ''
accounts = []
account = {""}

@app.route('/register/', methods=['GET', 'POST'])
def register():
    # create user save usr to db then redirect to home
    form = registration_form()
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
            successful_insert = db.insert_user(usr)
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


@app.route('/<failed>', methods=['GET', 'POST'])
def login(failed):
    # change to jwt authentication
    form = login_form()
    if form.validate_on_submit():
        usrname = form.username.data
        pwd = form.pwd.data
        # v2 pwd set usr.set_password(pwd, False)

        # will output values some where im not sure where
        # %s might need changed
        flash('username: %s' % form.username.data)
        flash('plaintext pw: %s' % form.pwd.data)
        isMatch = User.verify_password(usrname, pwd)
        if isMatch:
            return redirect(url_for('home', usrname=usrname))
        # might be redundant
        else:
            return render_template('login_html', failed='failed')
    else:
        return render_template('login.html', failed='unknown')


@app.route('/home/<usrname>')
def home(usrname):
    return render_template('home.html')


@app.route('/manage/<usrname>', methods=['GET', 'POST'])
def manage(usrname):
    # get accounts then create list of all accounts
    account = Account()
    return render_template('manage.html')


@app.route('/generator/', methods=['GET', 'POST'])
def generator():
    form = generator_form()
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
            return render_template('generator.html')
        else:
            return render_template('generator.html')
    return render_template('generator.html')