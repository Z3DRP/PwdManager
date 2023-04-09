from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class GeneratorForm(FlaskForm):
    # need to add validation that the number of characters doesnt go over len
    password_length = IntegerField('Length', validators=[DataRequired()])
    letter_count = IntegerField('Letter Count', validators=[DataRequired()])
    number_count = IntegerField('Number Count')
    symbol_count = IntegerField('Symbol Count')
    generated_password = StringField()
    generate = SubmitField('Generate')
    if generated_password is not None:
        password_generated = True