from flask import Blueprint, render_template, session
from flask_login import current_user
from .auth import login_required

views = Blueprint('views', __name__)

#root
@views.route('/') # home page aka website {domain}/ 
@login_required
def home(): # whatevers in here will run first for ^
    return render_template("home.html", session=session)

@views.route('/library') # home page aka website {domain}/ 
@login_required
def library(): # whatevers in here will run first for ^
    return render_template("library.html", session=session)

@views.route('/profile') # home page aka website {domain}/ 
@login_required
def profile(): # whatevers in here will run first for ^
    return render_template("profile.html", session=session)


