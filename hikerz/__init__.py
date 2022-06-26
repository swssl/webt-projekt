from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from os import urandom
from hikerz.db import *
from .views import views
from .api import api


app = Flask(__name__)
app.secret_key = urandom(12)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Blueprints registration
app.register_blueprint(views)
app.register_blueprint(api)
db.init_app(app)

# Flask-Migrate setup
migrate = Migrate(app, db, render_as_batch=True)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "views.login"


@login_manager.user_loader
def user_loader(username):
    return User.query.get(username)
