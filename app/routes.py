from app import App
from flask import render_template
from flask import url_for


@App.route('/login')
@App.route('/')
def login():
    return render_template('index.html')


@App.route('/register')
def register():
    return render_template('register.html')


@App.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')


