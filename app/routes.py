from app import App, db
from flask import render_template
from flask import url_for, redirect, Response
from flask import g                             # special object
from app.forms import LoginForm
from app.forms import RegisterForm
from app.forms import ForgotPasswordForm
from app.forms import EditProfileFrom
from app.forms import Boards
from app.forms import EditUsers
from flask_login import current_user, login_user# current_user
from flask_login import login_required
from flask_login import logout_user
from app.models import User, Role, Cards, Dht11
from flask import request, flash
from werkzeug.urls import url_parse
from app.config import Config
import json
import time
from datetime import datetime
from random import randint

temp = []
count = 0

@App.route('/login', methods=['GET', 'POST'])
@App.route('/', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form_login = LoginForm()
    #who_user =""
    if form_login.validate_on_submit():
        user = User.query.filter_by(email=form_login.email.data).first()
        # print('user role!!! :', user.role)
        # who_user = user
        if user is None:
            flash('Please register first ')
            return redirect(url_for('login'))
        login_user(user, remember=form_login.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('dashboard')
        return redirect(next_page)
    return render_template('index.html', form=form_login, title="Login")


@App.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:  # redirect the user if he is authenticated
        return redirect(url_for('dashboard'))
    admin_role = Role(name="admin")
    user_role = Role(name="user")
    form_register = RegisterForm()
    admin = form_register.email.data

    print("email entered", admin)
    if form_register.validate_on_submit():

        if admin == Config.ADMIN:
            user_reg = User(firstname=form_register.firstname.data, lastname=form_register.lastname.data,
                            email=form_register.email.data, password=form_register.password.data, admin= True)
            user_reg.set_password(form_register.password.data)
        else:
            user_reg = User(firstname=form_register.firstname.data, lastname=form_register.lastname.data,
                            email=form_register.email.data, password=form_register.password.data, admin=False)
            user_reg.set_password(form_register.password.data)
        db.session.add(user_reg)
        db.session.commit()
        flash('Login requested for user {} {}'.format(form_register.firstname.data, form_register.lastname.data))

        return redirect(url_for('login'))

    return render_template('register.html', form=form_register, title="Register")


@App.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@App.route('/forgot_password_request')
def forgot_password_request():
    form_forgot_password = ForgotPasswordForm()
    return render_template('forgot_password.html', form=form_forgot_password, title="Reset_Password_Request")


@App.route('/dashboard', methods = ['GET', 'POST'])
@login_required    # protect this page against unauthenticated user
def dashboard():
    global count
    actives = [1, 0, 0, 0]
    form = Boards()
    # user
    user_profile = User.query.filter_by(email=current_user.email).first()
    # cards the user have
    cards_ = Cards.query.filter_by(owner=user_profile).all()
    print("cardes: ", cards_)
    admin_email = Config.ADMIN
    print("who is the user ", user_profile)
    if form.validate_on_submit():
        c = Boards(type_=form.type_card.data, owner=user_profile)
        print(c)
        db.session.add(c)
        db.session.commit()

        return redirect(url_for('dashboard'))

    #r = request.form['1'].strip()
    # c_delate = Card.query.get(2)
    # c_delate.delete()


    #print("nb cards", cards)
    #cards = Card
    return render_template('dashboard.html', actives=actives, cards=cards_, admin_email=admin_email, user=user_profile, title="dashboard", form=form)


@App.route('/chart_data_temperature')
def chart_data_temperature():
    def generate():
        while True:
            global temp
            temperature_list = Dht11.query.all()
            t = temperature_list.pop().temperature
            # print(len(temperature_list) - 1, t)

            print(temperature_list.pop().temperature, temperature_list.pop().id)
            json_data = json.dumps(
                {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                 'value': t})
            #temp.append(t)
            yield "data:" + json_data + "\n\n"
            time.sleep(7)
            #print(temp)
    return Response(generate(), mimetype='text/event-stream')


@App.route('/dht11')
@login_required
def dht11():
    actives = [0, 1, 0, 0]  # dasboard, dht11, gaz
    return render_template('dht11.html', actives=actives, title=" Temperature ", time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


@App.route('/humidity')
@login_required
def humidity():
    actives = [0, 0, 1, 0]
    return render_template('humidity.html', actives=actives, title="Humidity")


@App.route('/gaz')
@login_required
def gaz():
    actives = [0, 0, 0, 1]
    return render_template('gaz.html', actives=actives, title="gaz")


@App.route('/users_edit', methods = ['GET', 'POST'])
@login_required
def users_edit():
    actives = [0, 0, 0, 0]
    edit_form = EditUsers()
    users = User.query.all()
    return render_template('users_edit.html', title ="Users_edit", actives=actives, users= users, time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), form=edit_form)


@App.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileFrom()
    if form.validate_on_submit():
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.password = form.password.data
        current_user.password_confirm = form.password_confirm.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('edit_profile.html', title="Edit_profile", form=form)


@App.before_request
def before_request():
    g.user = current_user                       # for user accessible through g.user
    if current_user.is_authenticated:           # add last seen time update
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
