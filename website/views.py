from flask import Blueprint, render_template, session, current_app, request, redirect, url_for
from flask_login import current_user
from .auth import login_required

views = Blueprint('views', __name__)

#root
@views.route('/') # home page aka website {domain}/ 
def home(): # whatevers in here will run first for ^
    return render_template("home.html", session=session)

@views.route('/profile') # home page aka website {domain}/ 
@login_required
def profile(): # whatevers in here will run first for ^
    return render_template("profile.html", session=session)

@views.route('/drive') # home page aka website {domain}/ 
@login_required
def drive(): # whatevers in here will run first for ^
    return render_template("drive.html", session=session)


@views.route('/library', methods=['GET', 'POST'])
def library():

    if 'images' not in session or session['images'] == []:
        session["images"] = current_app.config['DBM'].retrievePhotos()
    images = session["images"]

    if request.method == 'POST' and request.form['search'] != "":
        search = request.form['search']
        images = current_app.config['MM'].findImages(search, images, 5)
        #return redirect(url_for('library', session=session,  images=images))
    
    return render_template("library.html", session=session,  images=images)

