import datetime

from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError


class UserActivationForm(FlaskForm):
    name_on_card = StringField('Name on Card', validators=[DataRequired()])
    card_number = StringField('Card Number', validators=[DataRequired(), Length(min=16, max=16)])
    card_month = SelectField('Month of Expiry', validators=[DataRequired()])
    card_year = SelectField('Year of Expiry', validators=[DataRequired()])
    cvv_cvc = StringField('CVV/CVC Number', validators=[DataRequired(), Length(min=3, max=3)])
    submit = SubmitField('Save Card')

    def validate_card_number(self, card_number):
        if card_number.data != '4242424242424242':
            raise ValidationError('Wrong card number.')

    def validate_card_month(self, card_month):
        if card_month.data != '02':
            raise ValidationError('Wrong month.')

    def validate_card_year(self, card_year):
        if card_year.data != '2023':
            raise ValidationError('Wrong year.')

    def validate_cvv_cvc(self, cvv_cvc):
        if cvv_cvc.data != '123':
            raise ValidationError('Wrong CVV/CVC number.')

    def validate_name_on_card(self, name_on_card):
        if name_on_card.data != (current_user.first_name + ' ' + current_user.last_name):
            raise ValidationError('Name on card and name on profile are not the same.')
