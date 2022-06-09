from flask import Blueprint, render_template, redirect, request, jsonify
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

def manufactureSampleRoutes():
    route1 = Route(
        'Supertreck 2022', 
        'Dieser Treck ist super!', 
        './static/routes/example01.gpx',
        'bild1.jpeg',
        3,
        '11.123333290123456', '17.809987653214267')
    route2 = Route(
        'Zugspitze', 
        'Durch das Höllental auf die Zugspitze. Über Höllentalklamm, Gletscher und Klettersteig zum Gipfel. Trittsicherheit, solide Kondition und Schwindelfreiheit sind von Vorteil.', 
        './static/routes/zugspitze.gpx',
        'bild3.jpeg',
        5,
        '1.123456890123456', '17.809876543214267')
    route3 = Route(
        'GR20-E1', 
        'Der härteste Fernwanderweg Europas - Etappe 1', 
        './static/routes/gr20_etappe1.gpx',
        'bild12.jpeg',
        4,
        '8.854634646715482', '42.50634681278886')
    route4 = Route(
        'Entspannter Spaziergang', 
        'Zum entspannen', 
        './static/routes/test03.gpx',
        'bild5.jpeg',
        1,
        '82.851234567715482', '42.50634681278886')

    db.session.add(route1)
    db.session.add(route2)
    db.session.add(route3)
    db.session.add(route4)
    db.session.commit()
    print("in db")

@views.route('/routeoverview')
def routeOverview():    

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

    touren = Route.query.all()
    print(touren)

    return render_template('alleTouren.html', touren=touren, koordinaten=koordinaten)

@views.route('/routeoverview/tourenInNaehe/<posLon>/<posLat>')
def aktuellerStandort(posLon, posLat):
    #standort = '{"lon":'+str(posLon)+', "lat":'+str(posLat)+'}'

    #touren aus db holen
    touren = Route.query.all()
    print(touren)

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

    #naechste routen ermitteln
    naechsteRouten = {"routen": []}
    for k in koordinaten:
        if len(naechsteRouten["routen"])<1:#noch kein elemt in der liste
            dist = ((koordinaten[k][0]-float(posLon))**2) + ((koordinaten[k][1]-float(posLat))**2)
            naechsteRouten["routen"].append({"title":k, "pfad":touren[k], "distanz":dist})

        if len(naechsteRouten["routen"])<6:#liste ist noch nicht voll
            dist = ((koordinaten[k][0]-float(posLon))**2) + ((koordinaten[k][1]-float(posLat))**2)
            #print(naechsteRouten)
            naechsteRouten["routen"].append({"title":k, "pfad":touren[k], "distanz":dist})#neuen platz am ende einfügen

            for c,i in enumerate(naechsteRouten["routen"]):#an der passenden stelle der groesse nach sortiert einfuegen
                if i["distanz"] > dist:

                    for j in range(len(naechsteRouten["routen"])-1, c+1, -1):#alle um einen nach hinten verschieben
                        naechsteRouten["routen"][j] = naechsteRouten["routen"][j-1]

                    naechsteRouten["routen"][c] = {"title":k, "pfad":touren[k], "distanz":dist}#an aktuelle position die neue route einfuegen

                    break
        
        else:#liste ist zwar schon voll koennte aber naeher als eine andere route sein

            dist = ((koordinaten[k][0]-float(posLon))**2) + ((koordinaten[k][1]-float(posLat))**2)

            for c,i in enumerate(naechsteRouten["routen"]):#an der passenden stelle der groesse nach sortiert einfuegen
                if i["distanz"] > dist:

                    for j in range(len(naechsteRouten["routen"])-1, c+1, -1):#alle um einen nach hinten verschieben
                        naechsteRouten["routen"][j] = naechsteRouten["routen"][j-1]

                    naechsteRouten["routen"][c] = {"title":k, "pfad":touren[k], "distanz":dist}#an aktuelle position die neue route einfuegen

                    break

    return jsonify(naechsteRouten)

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


