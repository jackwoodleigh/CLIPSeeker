from flask import Blueprint, render_template

views = Blueprint('views', __name__)

#root
@views.route('/') # home page aka website {domain}/ 
def home(): # whatevers in here will run first for ^
    return render_template("home.html")