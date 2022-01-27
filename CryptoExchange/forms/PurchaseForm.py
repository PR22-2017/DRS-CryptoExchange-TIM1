import datetime

from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, HiddenField, Label
from wtforms.validators import DataRequired, Length, ValidationError


class PurchaseForm(FlaskForm):
    balance = StringField('Balance')
    currencies = SelectField('Crypto Currency', validators=[DataRequired()])
    prices = SelectField('Crypto Price', validators=[DataRequired()])
    quantity = StringField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Purchase Crypto')

    def validate_quantity(self, quantity):
        if current_user.balance < (float(quantity.data) * float(self.prices.data)):
            raise ValidationError('Not enough balance.')
        if float(quantity.data) <= 0:
            raise ValidationError('Please input number greater than 0')
