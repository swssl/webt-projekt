from flask import Blueprint, render_template, redirect, request
from flask_login import current_user, login_required, login_user, logout_user
from .db import *
from .forms import *

# Hier stehen die URL-Endpunkte/Routes

views = Blueprint("views", __name__, template_folder="templates")

@views.route('/hello')
def index():
    return render_template('base.html')

@views.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # redirect to home if user is already logged in
        return redirect("hello")
    form = LoginForm()
    if form.validate_on_submit():  # if valid data ist send by POST:
        user = User.query.get(form.data['user_name'])  # query user from db
        login_user(user)
        return redirect("hello")
    return render_template('login.html', login_form=form)

@views.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(form.data['user_name'],
                        form.data["email"], form.data["password"], 1) # create new user
        db.session.add(new_user)
        db.session.commit()     # write new user to db
        return redirect("login")
    return render_template('register.html', registration_form=form)

@views.route('/logout')
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect("login")
