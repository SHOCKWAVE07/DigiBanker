from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
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