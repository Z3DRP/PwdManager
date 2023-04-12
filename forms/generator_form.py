from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class GeneratorForm(FlaskForm):
    # need to add validation that the number of characters doesnt go over len
    pwd_length = IntegerField('Length', validators=[DataRequired(), NumberRange(min=0, max=100)], default=16)
    letter_count = IntegerField('Letter Count', validators=[DataRequired(), NumberRange(min=0, max=100)], default=8)
    number_count = IntegerField('Number Count', validators=[DataRequired(), NumberRange(min=0, max=100)], default=4)
    symbol_count = IntegerField('Symbol Count', validators=[DataRequired(), NumberRange(min=0, max=100)], default=4)
    generated_pwd = StringField()
    generate = SubmitField('Generate')
