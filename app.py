from flask import Flask, render_template

app = Flask(__name__)
usrID = ''

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/home/')
def home():
    return render_template('home.html')

@app.route('/manage/<int:usrid>')
def manage(usrid):
    return render_template('manage.html')

@app.route('/generator/')
def generator():
    return render_template('generator.html')