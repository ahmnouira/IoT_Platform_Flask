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



@App.route('/dashboard')
def dashboard():
    actives = [1, 0, 0, 0]
    return render_template('dashboard.html', actives=actives)


@App.route('/dht11')
def dht11():
    actives = [0, 1, 0, 0] # dasboard, dht11, gaz
    return render_template('dht11.html', actives=actives)


@App.route('/humidity')
def humidity():
    actives = [0, 0, 1, 0]
    return render_template('humidity.html', actives=actives, title="Gaz")


@App.route('/gaz')
def gaz():
    actives = [0, 0, 0, 1]
    return render_template('gaz.html', actives=actives, title="Gaz")

