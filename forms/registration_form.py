from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email Address', validators=[DataRequired(), Email()])
    pwd = PasswordField('Password', validators=[DataRequired()])
    confirm_pwd = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('pwd', message='Passwords do not match')])
    submit = SubmitField('Submit')
