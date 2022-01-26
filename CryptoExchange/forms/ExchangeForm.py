from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FloatField, HiddenField
from wtforms.validators import DataRequired, ValidationError


class ExchangeForm(FlaskForm):
    from_crypto = SelectField('From Crypto currency', validators=[DataRequired()])
    from_price = SelectField('Selected Crypto price', validators=[DataRequired()])
    from_balance = SelectField('Balance', validators=[DataRequired()])
    from_quantity = FloatField('Quantity to Exchange', validators=[DataRequired()])
    to_crypto = SelectField('To Crypto currency', validators=[DataRequired()])
    to_price = SelectField('Selected Crypto price', validators=[DataRequired()])
    to_quantity = HiddenField('Quantity in New Currency')
    submit = SubmitField('Convert Crypto')

    def validate_from_quantity(self, from_quantity):
        if float(from_quantity.data) <= 0 or float(self.from_balance.data) < float(from_quantity.data):
            raise ValidationError('Quantity must be more than 0, but less than available balance.')
