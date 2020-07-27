from flask import Blueprint, render_template, url_for, request, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User,Bars
from . import db
from flask_login import login_user,logout_user,login_required
import random

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    username= request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(username=username).first()
    barUser = Bars.query.filter_by(username=username).first()

    if not user and not barUser:
        flash('No user found in either table. Please try again.')
        return redirect(url_for('auth.login'))

    if user:
        print(user.password, flush= True)
        if not user.password == password:
            flash('Incorrect user credentials. Please try again.')
            return redirect(url_for('auth.login'))
        login_user(user, remember=remember)
        return redirect(url_for('main.profile'))

    if barUser:
        print(barUser.password, flush=True)
        if not barUser.password == password:
            flash('Incorrect bar credentials. Please try again.')
            return redirect(url_for('auth.login'))
        login_user(barUser, remember=remember)
        return redirect(url_for('main.profileBar'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    name = request.form.get('name')
    username = request.form.get('username')
    password = request.form.get('password')
    print("MADE IT PAST FORM PASSWORD", flush = True)
    user = Bars.query.filter_by(username=username).first() #if this returns user the user already exists
    print("MADE IT PAST THE QUERY", flush = True)
    if user:
        flash('Username already exists')
        return redirect(url_for('auth.signup'))
    if not password:
        flash('Please enter a password')
        return redirect(url_for('auth.signup'))
    id = random.randint(30000,50000)
    new_user = Bars(id=id,username=username,password=password,name=name, accountType='bar')

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))