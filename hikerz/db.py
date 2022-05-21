from enum import unique
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# In dieser Datei liegen die Datenbankklassen

class Tour(db.Model):
    __tablename__ = 'Route'

    routenID = db.Column(db.String(45), primary_key=True, unique=True)
    bezeichnung = db.Column(db.String(45), nullable=False)
    weg = db.Column(db.String(45), nullable=False)
    vorschaubild = db.Column(db.String(45),  nullable=False)

class Highlight(db.Model):
    __tablename__ = 'HighlightInRoute'

    routenID = db.Column(db.String(45), primary_key=True)
    highlights = db.Column(db.String(45), nullable=False, unique=True)
    password = db.Column(db.String(45), nullable=False)
    rolle = db.Column(db.Integer(),  nullable=False)
    isLoggedIn = db.Column(db.Boolean, nullable=False, default=False)