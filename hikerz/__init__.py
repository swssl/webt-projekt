from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from hikerz.db import *
from .views import views


app = Flask(__name__)
app.secret_key = b'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.register_blueprint(views)
db.init_app(app)
migrate = Migrate(app, db, render_as_batch=True)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "views.login"


@login_manager.user_loader
def user_loader(username):
    return User.query.get(username)
