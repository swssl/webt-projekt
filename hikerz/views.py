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

    koordinaten = {}
    koordinaten["Tour1"] = [8.5267646, 52.0268666 ]
    koordinaten["Tour2"] = [8.5266546, 52.0161666 ]
    koordinaten["Tour3"] = [8.5266346, 52.0164566 ] 
    koordinaten["Tour4"] = [9.5278646, 52.0148666 ]
    koordinaten["Tour5"] = [8.5267346, 52.0168466 ]
    koordinaten["Tour6"] = [8.5266846, 51.0168266 ] 
    koordinaten["Tour7"] = [8.5286646, 52.0168466 ]
    koordinaten["Tour8"] = [8.5264646, 52.0161666 ]
    koordinaten["Tour9"] = [8.5366646, 51.0164666 ]

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

    return render_template('alleTouren.html', touren=touren, test_user=test_user, koordinaten=koordinaten)

@views.route('/testRoute')
def testRoute():
    return "<h1>Testseite</h1>"



@views.route('/adminbereich')
def adminbereich():
    test_user = User("admin", "admin@localhost.org", "admin", 0)
    allUsers = {"user1":["Test1","1@1.de","admin"], "user2":["Test2","2@2.de","user"],"user3":["Test3","3@3.de","user"],"user4":["Test4","4@4.de","user"],"user5":["Test5","5@5.de","user"],"user6":["Test6","6@6.de","user"],"user7":["Test7","7@7.de","user"],"user8":["Test8","8@8.de","user"],"user9":["Test9","9@9.de","user"],"user10":["Test10","10@10.de","user"],"user11":["Test11","11@11.de","admin"], "user12":["Test12","12@12.de","user"],"user13":["Test13","13@13.de","user"],"user14":["Test14","14@41.de","user"],"user15":["Test15","15@51.de","user"],"user16":["Test16","16@16.de","user"],"user17":["Test17","71@17.de","user"],"user8":["Test18","18@18.de","user"],"user19":["Test19","91@19.de","user"],"user20":["Test20","20@20.de","user"]}
    return render_template("adminArea.html", allUsers=allUsers, test_user=test_user)


@views.route('/benutzerLoeschen/<userID>')
def adminbereichUserDelete(userID):
    print("Benutzer der geloescht werden soll:",userID)

    #loesch logik muss angepasst werden
    allUsers = {"user1":["Test1","1@1.de","admin"], "user2":["Test2","2@2.de","user"],"user3":["Test3","3@3.de","user"],"user4":["Test4","4@4.de","user"],"user5":["Test5","5@5.de","user"],"user6":["Test6","6@6.de","user"],"user7":["Test7","7@7.de","user"],"user8":["Test8","8@8.de","user"],"user9":["Test9","9@9.de","user"],"user10":["Test10","10@10.de","user"],"user11":["Test11","11@11.de","admin"], "user12":["Test12","12@12.de","user"],"user13":["Test13","13@13.de","user"],"user14":["Test14","14@41.de","user"],"user15":["Test15","15@51.de","user"],"user16":["Test16","16@16.de","user"],"user17":["Test17","71@17.de","user"],"user8":["Test18","18@18.de","user"],"user19":["Test19","91@19.de","user"],"user20":["Test20","20@20.de","user"]}
    loeschUser = None
    for u in allUsers:
        if allUsers[u][0] == userID:
            loeschUser = u
    if loeschUser is not None:
        del allUsers[loeschUser]

    test_user = User("admin", "admin@localhost.org", "admin", 0)
    
    return render_template("adminArea.html", allUsers=allUsers, test_user=test_user)


