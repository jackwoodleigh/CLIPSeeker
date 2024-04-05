from flask import Blueprint, render_template, session, current_app, request, redirect, url_for
from flask_login import current_user
from .auth import login_required
from functools import wraps
import json




def save_address(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session['last_page'] = request.url
        print(session['last_page'])
        return f(*args, **kwargs)
    return decorated_function

views = Blueprint('views', __name__)



#root
@views.route('/') 
@save_address
def home(): 
    return render_template("home.html", session=session)

@views.route('/profile')  
@login_required
@save_address
def profile(): 
    return render_template("profile.html", session=session)

@views.route('/drive')  
@login_required
@save_address
def drive(): 
    return render_template("drive.html", session=session)

@login_required
@save_address
@views.route('/library', methods=['GET', 'POST'])
def library():
    
    images = current_app.config['DBM'].retrievePhotos()
    
    
    if request.method == 'POST' and request.form['search'] != "":
        search = request.form['search']

        data = current_app.config['MM'].processImages(images)
        print("processed")
        current_app.config['DBM'].updateLibraryData(data)
        print("stored")
        data = current_app.config['DBM'].getLibraryData()
        print('retrieved')
        images = current_app.config['MM'].applyDataSearch(search, data, 5)
        print('searched')

        #images = current_app.config['MM'].findImages(search, images, 5)
        #return redirect(url_for('library', session=session,  images=images))
    
    return render_template("library.html", session=session,  images=images)

