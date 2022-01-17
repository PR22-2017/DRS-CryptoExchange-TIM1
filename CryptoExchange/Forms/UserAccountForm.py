from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from CryptoExchange.models.dbmodels import User


class UserAccountForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    country = SelectField('Country')
    phone = StringField('Phone', validators=[DataRequired()])
    submit = SubmitField('Sign up')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Do you already have an account?')

    def validate_phone(self, phone):
        if phone.data != current_user.phone:
            user = User.query.filter_by(phone=phone.data).first()
            if user:
                raise ValidationError('That phone number is taken. Please choose a different one.')
