from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, SelectField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, NumberRange
from app import db
from app.models import User
import sqlalchemy as sa

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')
        
class AccountForm(FlaskForm):
    mob_no = StringField('Mobile Number', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    pincode = StringField('Pincode', validators=[DataRequired()])
    pancard_no = StringField('Pancard Number', validators=[DataRequired()])
    account_type = SelectField('Account Type', choices=[('savings', 'Savings'), ('current', 'Current')], validators=[DataRequired()])
    submit = SubmitField('Create')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    mob_no = StringField('Mobile Number', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    pincode = StringField('Pincode', validators=[DataRequired()])
    submit = SubmitField('Confirm')

    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = db.session.scalar(sa.select(User).where(
                User.username == self.username.data))
            if user is not None:
                raise ValidationError('Please use a different username.')

class DepositForm(FlaskForm):
    amount = DecimalField('Amount', validators=[DataRequired(), NumberRange(min=0.01)])
    submit = SubmitField('Deposit')

class WithdrawForm(FlaskForm):
    amount = DecimalField('Amount', validators=[DataRequired(), NumberRange(min=0.01)])
    submit = SubmitField('Withdraw')

class TransferForm(FlaskForm):
    amount = DecimalField('Amount', validators=[DataRequired(), NumberRange(min=0.01)])
    receiver = StringField('To', validators=[DataRequired()])
    submit = SubmitField('Transfer')