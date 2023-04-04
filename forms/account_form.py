from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email

class AccountForm(FlaskForm):
    account_name = StringField('Account Name', validators=[DataRequired()])
    username = StringField('Username')
    email = EmailField('Email', validators=[Email()])
    pwd = StringField('Password')
    create = SubmitField('Create Account')
    # look up select fields and selectFields multiple if use select
    # will have to create json from fields then pass json into db method
    # extra_field = SelectField('Extra Field', choices=['Pin', 'Recovery Email'])
