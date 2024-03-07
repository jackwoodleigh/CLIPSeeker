from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

#root
@views.route('/') # home page aka website {domain}/ 
@login_required
def home(): # whatevers in here will run first for ^
    return render_template("home.html", logged_in=current_user.is_authenticated)

@views.route('/library') # home page aka website {domain}/ 
@login_required
def library(): # whatevers in here will run first for ^
    return render_template("library.html", logged_in=current_user.is_authenticated)

@views.route('/profile') # home page aka website {domain}/ 
@login_required
def profile(): # whatevers in here will run first for ^
    return render_template("profile.html", logged_in=current_user.is_authenticated)
