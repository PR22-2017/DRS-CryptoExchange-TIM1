from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email
from CryptoExchange.models.dbmodels import User


class TransactionForm(FlaskForm):
    receiver_email = StringField('Email', validators=[DataRequired(), Email()])
    currency = SelectField('Crypto currency', validators=[DataRequired()])
    balance = SelectField('Crypto balance', validators=[DataRequired()])
    quantity = StringField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Send Crypto')

    def validate_receiver_email(self, receiver_email):
        user = User.query.filter_by(email=receiver_email.data).first()
        if not user:
            raise ValidationError("User with entered email doesn't exists.")
        elif user.email == current_user.email:
            raise ValidationError("You can't make transfer to your own account.")

    def validate_quantity(self, quantity):
        if float(quantity.data) <= 0:
            raise ValidationError('Quantity need to be more than 0.')



