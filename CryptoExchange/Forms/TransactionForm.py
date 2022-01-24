import datetime

from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, HiddenField, Label
from wtforms.validators import DataRequired, Length, ValidationError, Email
from CryptoExchange.models.dbmodels import User


class TransactionForm(FlaskForm):
    receiver_email = StringField('Email', validators=[Email()])
    currency = HiddenField(validators=[DataRequired()])
    price = HiddenField(validators=[DataRequired()])
    currencies = SelectField('Crypto Currency', validators=[DataRequired()])
    quantity = StringField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Send Crypto')

    def validate_receiver_email(self, receiver_email):
        user = User.query.filter_by(email=receiver_email.data).first()
        if not user:
            raise ValidationError("User with entered email doesn't exists.")

    def validate_quantity(self, quantity):
        if current_user.balance < (float(self.quantity.data) * float(self.price.data) * 0.05):
            raise ValidationError('Not enough balance to.')



