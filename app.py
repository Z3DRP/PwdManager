from flask import Flask, render_template, redirect, url_for
from forms import login_form, registration_form
from models import User
from data_access import db

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
        usrname = form.username.data
        email = form.email.data
        pwd = form.pwd.data
        confirmed_pwd = form.confirm_pwd.data
        #EqaulTo validator validates passwords match dont need to add the logic
        try:
            usr = User(usrname, email, pwd)
            db.insert_user(usr)
            return redirect(url_for('home', usrname=usrname))
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
        isMatch = db.compare_passwords()
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

@app.route('/manage/<usrid>')
def manage(usrid):
    return render_template('manage.html')

@app.route('/generator/')
def generator():
    return render_template('generator.html')