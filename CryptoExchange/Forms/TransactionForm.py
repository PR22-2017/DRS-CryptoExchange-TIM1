import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, HiddenField, Label
from wtforms.validators import DataRequired, Length, ValidationError, Email


class TransactionForm(FlaskForm):
    reciever_email = StringField('Email', validators=[Email()])
    currencies = SelectField('Crypto Currency', validators=[DataRequired()])
    quantity = StringField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Submit Crypto Transaction')

