from flask import Blueprint, request, abort
from flask_login import login_required
from random import random
from time import sleep
from .db import User, Route
from .forms import *


api = Blueprint("api", __name__, template_folder="templates", url_prefix="/api")

@api.route('/routes/<username>')
@login_required
def routesApi(username):
    """Get the users routes in a lazy loading process

    Args:
        username (str): username to get routes of

    Returns:
        dict: jsonifyed dictionary as JSON response object
    """
    warnings = None
    try:
        start_index = int(request.args.get('first'))
    except Exception as e:
        start_index = None
        warnings = {"first": str(e)}
    try:
        end_index = int(request.args.get('last'))
    except Exception as e:
        warnings = {"last": str(e)}
        end_index = None
    
    data={"request": request.args, "response": [], "warnings": warnings}
    user = User.query.filter_by(username=username).first()
    if user:
        routes = Route.query.filter_by(creator=user.username).all()
        for r in routes[start_index:end_index]:
            data["response"].append(r.toDict())
    else:
        abort(404)
    sleep(random())
    return data