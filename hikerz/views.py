from flask import Blueprint, render_template, redirect, request
from db import User
from forms import *

# Hier stehen die URL-Endpunkte/Routes

views = Blueprint("views", __name__, template_folder="templates")

@views.route('/hello')
def index():
    test_user = User("admin", "admin@localhost.org", "admin", 0)
    return render_template('base.html', test_user = test_user)

@views.route('/login')
def login():
    test_user = User("admin", "admin@localhost.org", "admin", 0)
    return render_template('login.html', test_user=test_user)

@views.route('/addTour')
def addTour():
    return render_template('addTour.html') # maybe pass the users current location as default position