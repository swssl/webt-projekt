from flask import Blueprint, render_template, redirect, request, abort, url_for, jsonify
from flask_login import current_user, login_required, login_user, logout_user
from .db import *
from .forms import *

# Hier stehen die URL-Endpunkte/Routes

views = Blueprint("views", __name__, template_folder="templates")

@views.route('/')
def index():
    return render_template("home.html")


@views.route('/login', methods=['GET', 'POST'])
def login():
    # login view can be used for login an for confirmation
    if current_user.is_authenticated and not request.args.get("confirm"):  # redirect to home if user is already logged in
        return redirect(url_for("views.index"))
    form = LoginForm()
    if form.validate_on_submit():  # if valid data ist send by POST:
        user = User.query.filter_by(username=form.data['user_name']).first()  # query user from db
        login_user(user)
        return redirect(url_for("views.index"))
    return render_template('login.html', login_form=form, username_value=request.args.get('confirm'))

@views.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(form.data['user_name'],
                        form.data["email"], form.data["password"], 0) # create new user
        db.session.add(new_user)
        db.session.commit()     # write new user to db
        return redirect("login")
    return render_template('register.html', registration_form=form)

@views.route('/profil/<username>', methods=["GET", "POST"])
def profile(username):
    displayed_user = User.query.filter_by(username=username).first() # Get the users data from the database
    if not displayed_user:
        abort(404)
    form = AccountSettings()
    if form.validate_on_submit(): # If form is posted, look for changed data and forward it to the currentuser object
        if form.user_name.data:
            current_user.username = form.user_name.data
        if form.email.data:
            current_user.emailAdresse = form.email.data
        if form.new_password.data:
            current_user.password = form.new_password.data
        db.session.commit()
        return redirect(f"/login?confirm={current_user.username}") 
        # Redirect to login view because the login needs to be refreshed after changing the users username (primary key)
    # displayed_tours = Route.query.filter_by(creator=displayed_user.username).all()
    return render_template("profile.html", form=form, user = displayed_user)

@views.route('/logout')
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect("/")
    return render_template(url_for("views.index")) 


@views.route('/routeoverview')
def routeOverview():    
    touren = Route.query.all()
    #print(touren)

    return render_template('alleTouren.html', touren=touren)

@views.route('/routeoverview/tourenInNaehe/<posLon>/<posLat>')
def aktuellerStandort(posLon, posLat):
    #standort = '{"lon":'+str(posLon)+', "lat":'+str(posLat)+'}'

    #touren aus db holen
    touren = Route.query.all()
    print(touren)

    koordinaten = {}
    for t in touren:
        koordinaten[t.name] = [float(t.longitude), float(t.latitude)]

    #naechste routen ermitteln
    naechsteRouten = {"routen": []}
    for t in touren:
        if len(naechsteRouten["routen"])<1:#noch kein elemt in der liste
            dist = ((float(t.longitude)-float(posLon))**2) + ((float(t.latitude)-float(posLat))**2)
            naechsteRouten["routen"].append({"title":t.name, "pfad":t.previewImage, "distanz":dist})

        if len(naechsteRouten["routen"])<6:#liste ist noch nicht voll
            dist = ((float(t.longitude)-float(posLon))**2) + ((float(t.latitude)-float(posLat))**2)
            #print(naechsteRouten)
            naechsteRouten["routen"].append({"title":t.name, "pfad":t.previewImage, "distanz":dist})

            for c,i in enumerate(naechsteRouten["routen"]):#an der passenden stelle der groesse nach sortiert einfuegen
                if i["distanz"] > dist:

                    for j in range(len(naechsteRouten["routen"])-1, c+1, -1):#alle um einen nach hinten verschieben
                        naechsteRouten["routen"][j] = naechsteRouten["routen"][j-1]

                    naechsteRouten["routen"][c] = {"title":t.name, "pfad":t.previewImage, "distanz":dist}#an aktuelle position die neue route einfuegen

                    break
        
        else:#liste ist zwar schon voll koennte aber naeher als eine andere route sein

            dist = ((float(t.longitude)-float(posLon))**2) + ((float(t.latitude)-float(posLat))**2)

            for c,i in enumerate(naechsteRouten["routen"]):#an der passenden stelle der groesse nach sortiert einfuegen
                if i["distanz"] > dist:

                    for j in range(len(naechsteRouten["routen"])-1, c+1, -1):#alle um einen nach hinten verschieben
                        naechsteRouten["routen"][j] = naechsteRouten["routen"][j-1]

                    naechsteRouten["routen"][c] = {"title":t.name, "pfad":t.previewImage, "distanz":dist}#an aktuelle position die neue route einfuegen

                    break

    return jsonify(naechsteRouten)



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


