from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

#root
@views.route('/') # home page aka website {domain}/ 
@login_required
def home(): # whatevers in here will run first for ^
    return render_template("home.html")