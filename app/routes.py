from app import App
from flask import render_template
from flask import url_for
from app.forms import LoginForm
from app.forms import RegisterForm
from app.forms import ForgotPasswordForm

@App.route('/login', methods=['POST', 'GET'])
@App.route('/', methods=['POST', 'GET'])
def login():
    form_login = LoginForm()
    return render_template('index.html', form=form_login, title="Login")


@App.route('/register')
def register():
    form_register = RegisterForm()
    return render_template('register.html', form=form_register, title="Register")


@App.route('/forgot_password_request')
def forgot_password_request():
    form_forgot_password = ForgotPasswordForm()
    return render_template('forgot_password.html', form=form_forgot_password, title="Reset_Password_Request")


