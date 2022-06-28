import os
import gpxpy.gpx
from geopy.distance import geodesic
from flask import Blueprint, render_template, redirect, request, abort, url_for, jsonify
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from .db import *
from .forms import *



views = Blueprint("views", __name__, template_folder="templates")

@views.route('/')
def index():
    """Render homepage. Differentiation between a usere's and anonymous access is done in the template
        Author: Simon Wessel
    """
    return render_template("home.html")

@views.route('/login', methods=['GET', 'POST'])
def login():
    """Render login form for user authentication. If a 403 error occurs, we get redirected here. Same if user chages his/her username
        Author: Simon Wessel
    """
    if current_user.is_authenticated and not request.args.get("confirm"):  # redirect to home if user is already logged in
        return redirect(url_for("views.index"))
    form = LoginForm()
    if form.validate_on_submit():  # if valid data is send by POST request:
        user = User.query.filter_by(username=form.data['user_name']).first()  # query user from db
        login_user(user)
        return redirect(url_for("views.index"))
    return render_template('login.html', login_form=form, username_value=request.args.get('confirm'))

@views.route('/register', methods=["GET", "POST"])
def register():
    """Render registration form to add a new account to the db.
        Author: Simon Wessel
    """
    form = RegistrationForm()
    if form.validate_on_submit():       # Proof if data is valid and user doesnt already exist
        new_user = User(form.data['user_name'],
                        form.data["email"], form.data["password"], 0) # Create new user object
        db.session.add(new_user)
        db.session.commit()     # Write new user to db
        return redirect("login")
    return render_template('register.html', registration_form=form)

@views.route('/profil/<username>', methods=["GET", "POST"])
def profile(username):
    """Render user profile. If it is current_users one, he/she can edit the data. Author: Simon Wessel

    Args:
        username (str): Requested username
    """
    displayed_user = User.query.filter_by(username=username).first() # Get the users data from the database
    if not displayed_user:  # If user wasnt found in the db, display an 404 error
        abort(404)
    form = AccountSettings()
    if form.validate_on_submit(): # If form is POSTed, look for changed data and forward it to the current_user object
        if form.user_name.data:
            current_user.username = form.user_name.data
        if form.email.data:
            current_user.emailAdresse = form.email.data
        if form.new_password.data:
            current_user.password = generate_password_hash(form.new_password.data)
        db.session.commit()
        return redirect(f"/login?confirm={current_user.username}") # Redirect to login view because the login needs to be refreshed after changing the users username (for technical reasons, data is saved beforehand)
    # displayed_tours = Route.query.filter_by(creator=displayed_user.username).all() 
    return render_template("profile.html", form=form, user = displayed_user)#, displayed_tours = displayed_tours)

@views.route('/logout')
@login_required
def logout():
    """URL to call in order to log out. Redirect to homepage. Author: Simon Wessel
    """
    logout_user()
    return redirect("/")

@views.route('/routeoverview')
def routeOverview():    
    #alle Touren aus der Datenbank holen
    touren = Route.query.all()

    return render_template('alleTouren.html', touren=touren)


@views.route('/routeoverview/tourenInNaehe/<posLon>/<posLat>')
def aktuellerStandort(posLon, posLat):
    #touren aus db holen
    touren = Route.query.all()

    #naechste routen ermitteln
    naechsteRouten = {"routen": []}
    for t in touren:
        if len(naechsteRouten["routen"])<1:#noch kein elemt in der liste
            dist = ((float(t.longitude)-float(posLon))**2) + ((float(t.latitude)-float(posLat))**2)
            naechsteRouten["routen"].append({"title":t.name, "pfad":t.previewImage, "distanz":dist})

        elif len(naechsteRouten["routen"])<6:#liste ist noch nicht voll
            dist = ((float(t.longitude)-float(posLon))**2) + ((float(t.latitude)-float(posLat))**2)
            naechsteRouten["routen"].append({"title":t.name, "pfad":t.previewImage, "distanz":dist})

            #mittels bubblesort die liste sortieren
            for i in range(len(naechsteRouten["routen"])-1):
                for j in range(0, len(naechsteRouten["routen"])-1):
                    if naechsteRouten["routen"][j]["distanz"] > naechsteRouten["routen"][j+1]["distanz"]:
                        help = naechsteRouten["routen"][j]
                        naechsteRouten["routen"][j] = naechsteRouten["routen"][j+1]
                        naechsteRouten["routen"][j+1] = help
                    
        
        else:#liste ist zwar schon voll koennte aber naeher als eine andere route sein
            dist = ((float(t.longitude)-float(posLon))**2) + ((float(t.latitude)-float(posLat))**2)

            if dist < naechsteRouten["routen"][5]["distanz"]:
                naechsteRouten["routen"][5] = {"title":t.name, "pfad":t.previewImage, "distanz":dist}#groesstes ueberschreiben

                #neu sortieren
                for i in range(len(naechsteRouten["routen"])-1):
                    for j in range(0, len(naechsteRouten["routen"])-1):
                        if naechsteRouten["routen"][j]["distanz"] > naechsteRouten["routen"][j+1]["distanz"]:
                            help = naechsteRouten["routen"][j]
                            naechsteRouten["routen"][j] = naechsteRouten["routen"][j+1]
                            naechsteRouten["routen"][j+1] = help

            

    return jsonify(naechsteRouten)

@views.route('/adminbereich')
@login_required
def adminbereich():
    if current_user.rolle != 1:
        abort(401)
    allUsers = User.query.all() 
    
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


@views.route('/deleteRoute/<routeId>')
@login_required
def deleteRoute(routeId):
    """Deletes a route.\n
        This is done by deleting all referencing items from the database:
        - route-images
        - tags of route
        - highlights
        - highlight-images
        - reviews
        - review-images
        - the route itself

        Author: Simon Enns
    """
    # Only the creator of a route can delete a route
    if current_user.username == Route.query.filter(Route.id == routeId).first().creator:
        RouteImage.query.filter(RouteImage.routeId == routeId).delete()
        TagOfRoute.query.filter(TagOfRoute.routeId == routeId).delete()
        
        highlights = Highlight.query.filter(Highlight.routeId == routeId).all()
        Highlight.query.filter(Highlight.routeId == routeId).delete()
        for highlight in highlights:
            HighlightImage.query.filter(HighlightImage.highlightId == highlight.id)
        
        reviews = Review.query.filter(Review.routeId == routeId).all()
        Review.query.filter(Review.routeId == routeId).delete()
        for review in reviews:
            ReviewImage.query.filter(ReviewImage.reviewId == review.id).delete()
        
        Route.query.filter(Route.id == routeId).delete()

        db.session.commit()

        return redirect('/') # redirect to home after deletion
    
    return redirect(request.url)


@views.route('/addRoute', methods=['GET'])
@login_required
def addRoute():
    """Renders the HTML for adding a route.
        Author: Simon Enns
    """
    return render_template('addRoute.html', addRouteForm=AddRouteForm())


@views.route('/addRoute/upload', methods=['POST'])
def uploadNewRoute():
    """Creates a new route:
        - Uploads gpx- and image-files into the correspondig static-folder (from request)
        - reads first point from gpx-file and sets the start-latitude and start-longitude
        - instantiates a new Route and commits it to the database

        Author: Simon Enns
    """
    try:
        trailFile = request.files.get('trail')
        # 'secure_filename' prohibits invalid and/or potentially malicious filenames
        trailFile.save(os.path.join('hikerz/static/routes', secure_filename(trailFile.filename)))
        previewImageFile = request.files.get('previewImage')
        previewImageFile.save(os.path.join('hikerz/static/vorschaubilder', secure_filename(previewImageFile.filename)))

        try:
            f = open('hikerz/static/routes/' + trailFile.filename, 'r')
            gpxFile = gpxpy.parse(f)

            if len(gpxFile.tracks) != 0:
                track = gpxFile.tracks[0].segments[0]
                p = track.points[0] # first point = start point
            elif len(gpxFile.routes) != 0:
                track = gpxFile.routes[0]
                p = track.points[0] # first point = start point
            
            coords = (p.latitude, p.longitude)

        except: # if reading gpx-file fails -> return default coords
            coords = ('8.8395630534', '51.9115881915') # default: Coordinates of the Hermannsdenkmal

        newRoute = Route(
            request.form.get('name'),
            request.form.get('description'),
            '/static/routes/' + trailFile.filename,
            '/static/vorschaubilder/' + previewImageFile.filename,
            int(request.form.get('technicalDifficulty')),
            int(request.form.get('stamina')),
            calculateTrailDistance(track.points),
            int(request.form.get('duration')),
            coords[0], # longitude
            coords[1], # latitude
            current_user.username
        )

        db.session.add(newRoute)
        db.session.commit()
                
    except:
        return redirect('/addRoute')

    return redirect(f'/routeDetails/{ newRoute.id }')


def calculateTrailDistance(points) -> int:
    """Calculates the distance of the track from the passed list of treckpoints.
        Author: Simon Enns
    """
    distance = 0
    if len(points) > 0:
        for i in range(len(points) - 1):
            if points[i + 1]:
                distance += geodesic(getPoint(points[i]), getPoint(points[i + 1])).meters
    return int(distance)


def getPoint(p) -> tuple:
    """Get point as tuple in format '(lat, lon)'
        Author: Simon Enns
    """
    return (p.latitude, p.longitude)


@views.route('/routeDetails/<routeId>', methods=['GET', 'POST'])
def routeDetails(routeId):
    route = Route.query.filter_by(id=routeId).first()
    highlights = Highlight.query.filter(routeId == routeId).all()

    routeImageForm = AddRouteImageForm()
    addHighlightForm = AddHighlightForm()

    if routeImageForm.validate_on_submit():
        if request.method == 'POST':
            previewImageFile = request.files.get('routeImage')
            previewImageFile.save(os.path.join('hikerz/static/vorschaubilder', secure_filename(previewImageFile.filename)))

        newRouteImage = RouteImage(
            routeId,
            '/static/vorschaubilder/' + routeImageForm.data['image'],
            current_user.username
        )

        db.session.add(newRouteImage)
        db.session.commit()

        return redirect(f'/routeDetails/{route.id}')
    

    if addHighlightForm.validate_on_submit():
        if request.method == 'POST':
            previewImageFile = request.files.get('highlightPreviewImage')
            previewImageFile.save(os.path.join('hikerz/static/vorschaubilder', secure_filename(previewImageFile.filename)))


        newHighlight = Highlight(
            addHighlightForm.data['name'],
            addHighlightForm.data['description'],
            '/static/vorschaubilder/' + addHighlightForm.data['previewImage'],
            addHighlightForm.data['latitude'],
            addHighlightForm.data['longitude'],
            current_user.username
        )

        db.session.add(newHighlight)
        db.session.commit()


        return redirect(f'/routeDetails/{ route.id }')

    return render_template(
        'routeHighlights.html',
        highlights=highlights, 
        route=route, 
        routeImageForm=routeImageForm,
        addHighlightForm=addHighlightForm)



@views.route('/routeDetails/<routeId>/routeImages', methods=['GET', 'POST'])
def routeImages(routeId):
    route = Route.query.filter_by(id=routeId).first()
    images = RouteImage.query.filter_by(routeId=routeId).all()

    form = AddRouteImageForm()

    if form.validate_on_submit():
        newImage = RouteImage(
            routeId,
            '/static/vorschaubilder/' + form.data['image'],
            current_user.username
        )
        db.session.add(newImage)
        db.session.commit()

        return redirect(f'/routeDetails/{ routeId }/routeImages')

    return render_template('routeImages.html', images=images, route=route, routeImageForm=form)


@views.route('/routeDetails/<routeId>/highlights', methods=['GET', 'POST'])
def addRouteHighlight(routeId):
    route = Route.query.filter_by(id=routeId).first()
    highlights = Highlight.query.filter(routeId == routeId).all()
    form = AddHighlightForm()

    if form.validate_on_submit():
        newHighlight = Highlight(
            form.data['name'],
            form.data['description'],
            '/static/vorschaubilder/' + form.data['previewImage'],
            current_user.username
        )

        db.session.add(newHighlight)
        db.session.commit()

        return redirect(f'/routeDetails/{ route.id }/highlights')

    return render_template('routeHighlights.html', addHighlightForm=form, highlights=highlights, route=route)
