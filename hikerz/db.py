from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


# In dieser Datei liegen die Datenbankklassen

class User(db.Model):
    __tablename__ = 'User'

    username = db.Column(db.String(45), primary_key=True)
    emailAdresse = db.Column(db.String(45), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    rolle = db.Column(db.Integer(),  nullable=False)
    creatorOfRoute = db.relationship('Route', back_populates='creatorRelationship')
    creatorOfHighlight = db.relationship('Highlight', back_populates='creatorRelationship')
    creatorOfRouteImage = db.relationship('RouteImage', back_populates='creatorRelationship')
    creatorOfReview = db.relationship('Review', back_populates='creatorRelationship')
    member_since = db.Column(db.String(10), nullable=False, default="01.01.2022")

    def __init__(self, username, emailAdresse, password, rolle) -> None:
        super().__init__()
        self.username = username
        self.emailAdresse = emailAdresse
        self.password = generate_password_hash(password) # Store hashed password in db instead of plain text
        self.rolle = rolle
        self.member_since = dt.today().strftime("%d.%m.%Y")

    def check_password(self, pwd):
        return check_password_hash(self.password, pwd)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self.username

    def __repr__(self):
        return f"<User {self.username}>"


class Route(db.Model):
    __tablename__ = 'Route'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(45), nullable=False, default='Neue Route')
    description = db.Column(db.String(1024), nullable=False)
    trail = db.Column(db.String(45), nullable=False)
    previewImage = db.Column(db.String(255), nullable=False, default='PathToDefaultImage')
    technicalDifficulty = db.Column(db.Integer(), nullable=True)
    stamina = db.Column(db.Integer(), nullable=True)
    distance = db.Column(db.Integer(), nullable=False) # distance in meters
    duration = db.Column(db.Integer(), nullable=True) # could be calculated from the length of the trail and the average hiking speed
    longitude = db.Column(db.String(15), nullable=False)
    latitude = db.Column(db.String(15), nullable=False)
    creator = db.Column(db.String(45), db.ForeignKey('User.username'))
    creatorRelationship = db.relationship('User', back_populates='creatorOfRoute')
    highlightInRoute = db.relationship('HighlightInRoute', back_populates='route')
    routeImage = db.relationship('RouteImage', back_populates='route')
    tagOfRoute = db.relationship('TagOfRoute', back_populates='route')
    review = db.relationship('Review', back_populates='route')

    def __init__(self, name, description, trail, previewImage, technicalDifficulty, stamina, distance, duration, longitude, latitude, creator) -> None:
        super().__init__()
        self.name = name
        self.description = description
        self.trail = trail
        self.previewImage = previewImage
        self.technicalDifficulty = technicalDifficulty
        self.stamina = stamina
        self.distance = distance
        self.duration = duration
        self.longitude = longitude
        self.latitude = latitude
        self.creator = creator

    def __repr__(self):
        return f'<Route \
            "name" {self.name}, \
            "description" {self.description}, \
            "trail" {self.trail}, \
            "previewImage" {self.previewImage}, \
            "technicalDifficulty" {self.technicalDifficulty}, \
            "stamina" {self.stamina}, \
            "distance" {self.distance},\
            "duration" {self.duration}, \
            "longitude" {self.longitude}, \
            "latitude" {self.latitude}, \
            "creator" {self.creator}>'


class Highlight(db.Model):
    __tablename__ = 'Highlight'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(45), nullable=False, default='Neues Highlight')
    description = db.Column(db.String(1024), nullable=True)
    previewImage = db.Column(db.String(255), nullable=False, default='PathToDefaultImage')
    latitude =  db.Column(db.String(15), nullable=False)
    longitude = db.Column(db.String(15), nullable=False)
    creator = db.Column(db.String(45), db.ForeignKey('User.username'))
    creatorRelationship = db.relationship('User', back_populates='creatorOfHighlight')
    highlightInRoute = db.relationship('HighlightInRoute', back_populates='highlight')
    highlightImage = db.relationship('HighlightImage', back_populates='highlight')

    def __init__(self, name, description, previewImage, latitude, longitude, creator) -> None:
        super().__init__()
        self.name = name
        self.description = description
        self.previewImage = previewImage
        self.latitude = latitude
        self.longitude = longitude
        self.creator = creator

    def __repr__(self) -> str:
        return f'<Highlight \
            "name" {self.name}, \
            "description" {self.description}, \
            "previewImage" {self.previewImage}, \
            "latitude" {self.latitude}, \
            "longitude" {self.longitude}, \
            "creator" {self.creator}>'

class HighlightInRoute(db.Model):
    __tablename__ = 'HighlightInRoute'

    id = db.Column(db.Integer(), primary_key=True)
    routeId = db.Column(db.Integer(), db.ForeignKey('Route.id'))
    highlightId = db.Column(db.Integer(), db.ForeignKey('Highlight.id'))
    route = db.relationship('Route', back_populates='highlightInRoute')
    highlight = db.relationship('Highlight', back_populates='highlightInRoute')

    def __init__(self, routeId, highlightId) -> None:
        super().__init__()
        self.routeId = routeId
        self.highlightId = highlightId

    def __repr__(self) -> str:
        return f'<HighlightInRoute \
            "routeId" {self.routeId}, \
            "highlightId" {self.highlightId}>'


class RouteImage(db.Model):
    __tablename__ = 'RouteImages'

    id = db.Column(db.Integer(), primary_key=True)
    routeId = db.Column(db.Integer(), db.ForeignKey('Route.id'))
    image = db.Column(db.String(255), nullable=False)
    creator = db.Column(db.String(45), db.ForeignKey('User.username'))
    route = db.relationship('Route', back_populates='routeImage')
    creatorRelationship = db.relationship('User', back_populates='creatorOfRouteImage')

    def __init__(self, routeId, image, creator) -> None:
        super().__init__()
        self.routeId = routeId
        self.image = image
        self.creator = creator
    
    def __repr__(self) -> str:
        return f'<RouteImage \
            "routeId" {self.routeId}, \
            "image" {self.image}, \
            "creator" {self.creator}>'


class HighlightImage(db.Model):
    __tablename__ = 'HighlightImage'

    id = db.Column(db.Integer(), primary_key=True)
    image = db.Column(db.String(255), nullable=False)
    highlightId = db.Column(db.Integer(), db.ForeignKey('Highlight.id'))
    highlight = db.relationship('Highlight', back_populates='highlightImage')

    def __init__(self, highlightId, image) -> None:
        super().__init__()
        self.highlightId = highlightId
        self.image = image
    
    def __repr__(self) -> str:
        return f'<HighlightImage \
        "highlightId" {self.highlightId}, \
        "image" {self.image}>'


class TagOfRoute(db.Model):
    __tablename__ = 'TagOfRoute'

    id = db.Column(db.Integer(), primary_key=True)
    tag = db.Column(db.String(45), nullable=False, default='Default Tag')
    routeId = db.Column(db.Integer(), db.ForeignKey('Route.id'))
    route = db.relationship('Route', back_populates='tagOfRoute')

    def __init__(self, tag, routeId) -> None:
        super().__init__()
        self.tag = tag
        self.routeId = routeId
    
    def __repr__(self) -> str:
        return f'<TagOfRoute \
        "tag" {self.tag}, \
        "routeId" {self.routeId}>'


class Review(db.Model):
    __tablename__ = 'Review'

    id = db.Column(db.Integer(), primary_key=True)
    topic = db.Column(db.String(45), nullable=False)
    review = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Integer(), nullable=False) # 1-10
    helpful = db.Column(db.Integer(), nullable=False) # count of up-/downvotes
    creator = db.Column(db.String(45), db.ForeignKey('User.username'))
    routeId = db.Column(db.Integer(), db.ForeignKey('Route.id'))
    route = db.relationship('Route', back_populates='review')
    creatorRelationship = db.relationship('User', back_populates='creatorOfReview')
    reviewImage = db.relationship('ReviewImage', back_populates='review')

    def __init__(self, topic, review, rating, helpful, creator) -> None:
        super().__init__()
        self.topic = topic
        self.review = review
        self.rating = rating
        self.helpful = helpful
        self.creator = creator

    def __repr__(self) -> str:
        return f'<Review \
        "topic" {self.topic}, \
        "review" {self.review}, \
        "rating" {self.rating}, \
        "helpful" {self.helpful}, \
        "creator" {self.creator}>'


class ReviewImage(db.Model):
    __tablename__ = 'ReviewImage'

    id = db.Column(db.Integer(), primary_key=True)
    image = db.Column(db.String(255), nullable=False)
    reviewId = db.Column(db.Integer(), db.ForeignKey('Review.id'))
    review = db.relationship('Review', back_populates='reviewImage')

    def __init__(self, reviewId, image) -> None:
        super().__init__()
        self.reviewId = reviewId
        self.image = image
    
    def __repr__(self) -> str:
        return f'<ReviewImage \
        "reviewId" {self.reviewId}, \
        "image" {self.image}>'
