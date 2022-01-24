from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class AddBalanceForm(FlaskForm):
    current_balance = StringField('Current balance')
    balance_to_add = StringField('Balance to Add', validators=[DataRequired()])
    submit = SubmitField('Add Balance')

    def validate_balance_to_add(self, balance_to_add):
        if float(balance_to_add.data) <= 0:
            raise ValidationError('Enter more than $0.')
