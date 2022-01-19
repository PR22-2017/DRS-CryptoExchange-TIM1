import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, HiddenField, Label
from wtforms.validators import DataRequired, Length, ValidationError


class PurchaseForm(FlaskForm):
    balance = StringField('Balance')
    currencies = SelectField('Crypto Currency', validators=[DataRequired()])
    quantity = StringField('Quantity', validators=[DataRequired()])

    def validate_quantity(self, quantity):

        now = datetime.datetime.now()
        check = datetime.datetime(int(self.card_year.data), int(self.card_month.data)+1, 1) - datetime.timedelta(days=1)
        if check < now:
            raise ValidationError('Your card has expired, try using another one.')
