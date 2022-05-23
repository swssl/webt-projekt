from flask import Blueprint, render_template, redirect, request
from .db import User
from .forms import *


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


@views.route('/routeoverview')
def routeOverview():
    
    #das touren-dictionary muss nachher zu einer db-abfrage geaendert werden
    touren = {}#dictionary mit tourbezeichnung und pfad zu vorschaubild
    touren["Tour1"] = "bild1.jpeg"
    touren["Tour2"] = "bild2.jpeg"
    touren["Tour3"] = "bild3.jpeg"
    touren["Tour4"] = "bild4.jpeg"
    touren["Tour5"] = "bild5.jpeg"
    touren["Tour6"] = "bild6.jpeg"
    touren["Tour7"] = "bild7.jpeg"
    touren["Tour8"] = "bild8.jpeg"
    touren["Tour9"] = "bild9.jpeg"

    return render_template('alleTouren.html', touren=touren)


@views.route('/adminbereich')
def adminbereich():
    test_user = User("admin", "admin@localhost.org", "admin", 0)
    allUsers = {"user1":["Test1","1@1.de","admin"], "user2":["Test2","2@2.de","user"],"user3":["Test3","3@3.de","user"],"user4":["Test4","4@4.de","user"],"user5":["Test5","5@5.de","user"],"user6":["Test6","6@6.de","user"],"user7":["Test7","7@7.de","user"],"user8":["Test8","8@8.de","user"],"user9":["Test9","9@9.de","user"],"user10":["Test10","10@10.de","user"]}
    return render_template("adminArea.html", allUsers=allUsers, test_user=test_user)

