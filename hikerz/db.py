from os import unlink
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import null, nullslast

db = SQLAlchemy()


# In dieser Datei liegen die Datenbankklassen

class User(db.Model):
    __tablename__ = 'User'

    username = db.Column(db.String(45), primary_key=True)
    emailAdresse = db.Column(db.String(45), nullable=False, unique=True)
    password = db.Column(db.String(45), nullable=False)
    rolle = db.Column(db.Integer(),  nullable=False)

    def __init__(self, username, emailAdresse, password, rolle) -> None:
        super().__init__()
        self.username = username
        self.emailAdresse = emailAdresse
        self.password = password
        self.rolle = rolle

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

    id = db.Column(db.Integer(), primary_key=True, auto_increment=True)
    name = db.Column(db.String(45), nullable=False, default='Neue Route')
    description = db.Column(db.String(1024), nullable=False)
    trail = db.Column(db.String(45), nullable=False) # TODO: check what the correct data type is
    previewImage = db.Column(db.String(255), nullable=False, default='PathToDefaultImage')
    technicalDifficulty = db.Column(db.Integer(), nullable=True)
    stamina = db.Column(db.Integer(), nullable=True)
    duration = db.Column(db.Integer(), nullable=True) # could be calculated from the length of the trail and the average hiking speed
    highlightInRoute = db.relationship('HighlightInRoute', back_populates='route')
    routeImage = db.relationship('RouteImage', back_populates='route')
    tagOfRoute = db.relationship('TagOfRoute', back_populates='route')

    def __init__(self, name, description, trail, previewImage, technicalDifficulty, stamina, duration) -> None:
        super().__init__()
        self.name = name
        self.description = description
        self.trail = trail
        self.previewImage = previewImage
        self.technicalDifficulty = technicalDifficulty
        self.stamina = stamina
        self.duration = duration


class Highlight(db.Model):
    __tablename__ = 'Highlight'

    id = db.Column(db.Integer(), primary_key=True, auto_increment=True)
    name = db.Column(db.String(45), nullable=False, default='Neues Highlight')
    description = db.Column(db.String(1024), nullable=True)
    coordinates = db.Column(db.String(64), nullable=False) # TODO: check how to best store coordinates
    previewImage = db.Column(db.String(255), nullable=False, default='PathToDefaultImage')
    highlightInRoute = db.relationship('HighlightInRoute', back_populates='highlight')
    highlightImage = db.relationship('HighlighImage', back_populates='highlight')

    def __init__(self, name, description, coordinates, previewImage) -> None:
        super().__init__()
        self.name = name
        self.description = description
        self.coordinates = coordinates
        self.previewImage = previewImage



class HighlightInRoute(db.Model):
    __tablename__ = 'HighlightInRoute'

    id = db.Column(db.Integer(), primary_key=True, auto_increment=True)
    routeId = db.Column(db.Integer(), db.ForeignKey('route.id'))
    route = db.relationship('Route', back_populates='highlightInRoute')
    highlightId = db.Column(db.Integer(), db.ForeignKey('highlight.id'))
    highlight = db.relationship('Highlight', back_populates='highlightInRoute')

    def __init__(self, routeId, highlightId) -> None:
        super().__init__()
        self.routeId = routeId
        self.highlightId = highlightId


class RouteImage(db.Model):
    __tablename__ = 'RouteImages'

    id = db.Column(db.Integer(), primary_key=True, auto_increment=True)
    routeId = db.Column(db.Integer(), db.ForeignKey('route.id'))
    route = db.relationship('Route', back_populates='routeImage')
    image = db.Column(db.String(255), nullable=False)

    def __init__(self, routeId, image) -> None:
        super().__init__()
        self.routeId = routeId
        self.image = image


class HighlightImage(db.Model):
    __tablename__ = 'HighlightImage'

    id = db.Column(db.Integer(), primary_key=True, auto_increment=True)
    highlightId = db.Column(db.Integer(), db.ForeignKey('highlight.id'))
    highlight = db.relationship('Highlight', back_populates='highlightImage')
    image = db.Column(db.String(255), nullable=False)

    def __init__(self, highlightId, image) -> None:
        super().__init__()
        self.highlightId = highlightId
        self.image = image


class TagOfRoute(db.Model):
    __tablename__ = 'TagOfRoute'

    id = db.Column(db.Integer(), primary_key=True, auto_increment=True)
    tag = db.Column(db.String(45), nullable=False, default='Default Tag')
    routeId = db.Column(db.Integer(), db.ForeignKey('route.id'))
    route = db.relationship('Route', back_populates='tagOfRoute')

    def __init__(self, tag, routeId) -> None:
        super().__init__()
        self.tag = tag
        self.routeId = routeId


class Review(db.Model):
    __tablename__ = 'Review'

    id = db.Column(db.Integer(), primary_key=True, auto_increment=True)
    topic = db.Column(db.String(45), nullable=False)
    review = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Integer(), nullable=False) # 1-10
    helpful = db.Column(db.Integer(), nullable=False) # count of up-/downvotes
    reviewImage = db.relationship('ReviewImage', back_populates='review')

    def __init__(self, topic, review, rating, helpful) -> None:
        super().__init__()
        self.topic = topic
        self.review = review
        self.rating = rating
        self.helpful = helpful


class ReviewImage(db.Model):
    __tablename__ = 'ReviewImage'

    id = db.Column(db.Integer(), primary_key=True, auto_increment=True)
    reviewId = db.Column(db.Integer(), db.ForeignKey('review.id'))
    review = db.relationship('Review', back_populates='reviewImage')
    image = db.Column(db.String(255), nullable=False)

    def __init__(self, reviewId, image) -> None:
        super().__init__()
        self.reviewId = reviewId
        self.image = image


