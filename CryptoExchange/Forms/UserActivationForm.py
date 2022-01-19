import datetime
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
        now = datetime.datetime.now()
        check = datetime.datetime(int(self.card_year.data), int(self.card_month.data)+1, 1) - datetime.timedelta(days=1)
        if check < now:
            raise ValidationError('Your card has expired, try using another one.')
