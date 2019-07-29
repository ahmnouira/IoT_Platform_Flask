from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField,SubmitField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField(' Remember Password')
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    firstname = StringField('First name', validators=[DataRequired()])
    lastname = StringField('Last name', validators=[DataRequired()])
    email = StringField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class EditProfileFrom(FlaskForm):
    firstname = StringField('New first name ?', validators=[DataRequired()])
    lastname = StringField('New last name ?', validators=[DataRequired()])
    password = PasswordField('New password ?', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[EqualTo('password')])
    submit = SubmitField('Submit')


class ForgotPasswordForm(FlaskForm):
    email = StringField('Enter email address', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')


class Boards(FlaskForm):
    name = StringField('Name of the card', validators=[DataRequired()])
    submit = SubmitField('Create')


class EditCards(FlaskForm):
    submit = SubmitField('Delete')

