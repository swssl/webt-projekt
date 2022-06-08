from sys import flags
from flask import Blueprint, render_template, redirect, request, abort
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


    test_user = User("admin", "admin@localhost.org", "admin", 0)
    
    """touren = {}
    touren["Tour1"] = Route("Route1","Dies ist Route 1", "Weg", "bild1.jpeg", 1, 1, 20)
    touren["Tour2"] = Route("Route2","Dies ist Route 2", "Weg", "bild2.jpeg", 1, 1, 20)
    touren["Tour3"] = Route("Route3","Dies ist Route 3", "Weg", "bild3.jpeg", 1, 1, 20)
    touren["Tour4"] = Route("Route4","Dies ist Route 4", "Weg", "bild4.jpeg", 1, 1, 20)
    touren["Tour5"] = Route("Route5","Dies ist Route 5", "Weg", "bild5.jpeg", 1, 1, 20)
    touren["Tour6"] = Route("Route6","Dies ist Route 6", "Weg", "bild6.jpeg", 1, 1, 20)
    touren["Tour7"] = Route("Route7","Dies ist Route 7", "Weg", "bild7.jpeg", 1, 1, 20)
    touren["Tour8"] = Route("Route8","Dies ist Route 8", "Weg", "bild8.jpeg", 1, 1, 20)
    touren["Tour9"] = Route("Route9","Dies ist Route 9", "Weg", "bild9.jpeg", 1, 1, 20)"""

    return render_template('alleTouren.html', touren=touren, test_user=test_user)

@views.route('/testRoute')
def testRoute():
    return "<h1>Testseite</h1>"



@views.route('/adminbereich')
@login_required
def adminbereich():
    if current_user.rolle != 1:
        abort(401)
    allUsers = User.query.all() 
    #test_user = User("admin", "admin@localhost.org", "admin", 0)
    
    return render_template("adminArea.html", allUsers=allUsers)


@views.route('/benutzerLoeschen/<userID>')
@login_required
def adminbereichUserDelete(userID):
    if current_user.rolle == 1 and current_user.username == userID:#ein Admin darf sich nicht selber loeschen
        return redirect('/adminbereich')
    elif current_user.rolle == 1 and User.query.filter(User.username == userID).first().rolle == 1:#ein Admin darf keinen anderen Admin loeschen
        return redirect('/adminbereich')
    elif current_user.username == userID:#man darf sich selber ohne Adminrechte loeschen
        User.query.filter(User.username == userID).delete()
        db.session.commit()
        return redirect('/')#auf homepage verlinken
    elif current_user.rolle == 1:#ein Admin will einen normalen User loeschen
        #benutzer wird aus db geloescht
        User.query.filter(User.username == userID).delete()
        db.session.commit()    
        return redirect('/adminbereich')#auf adminbereich verlinken
    else:#ein nicht Admin will loeschen
        abort(401)


@views.route('/benutzerRechteErhoehen/<userID>')
@login_required
def adminbereichRechteErhoehen(userID):
    if current_user.rolle != 1:
        abort(401)

    #benutzer wird geupdated
    num_rows_updated = User.query.filter_by(username=userID).update(dict(rolle=1))
    db.session.commit()
    
    return redirect('/adminbereich')#auf adminbereich verlinken


@views.route('/benutzerRechteVerringern/<userID>')
@login_required
def adminbereichRechteVerringern(userID):
    if current_user.rolle != 1:
        abort(401)

    if current_user.username == userID:#man darf sich nicht selber die rechte wegnehmen
        return redirect('/adminbereich')#sonst koennten alle admins geloescht werden

    #benutzer wird aus db geloescht
    num_rows_updated = User.query.filter_by(username=userID).update(dict(rolle=0))
    db.session.commit()
    
    return redirect('/adminbereich')#auf adminbereich verlinken


