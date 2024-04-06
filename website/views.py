from flask import Blueprint, render_template, session, current_app, request, redirect, url_for
from flask_login import current_user
from .auth import login_required
from functools import wraps
import json
import numpy as np




def save_address(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session['last_page'] = request.url
        #print(session['last_page'])
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
    images = []
    if 'token' in session:
        ids, feature_data = current_app.config['DBM'].loadFileIdsToSession()

        if session['fileids']:
            photo_data = current_app.config['DBM'].retrievePhotos()
            # only allows photos that are up to date
            if photo_data != None and ids != []:
                images = [v for k, v in photo_data.items() if k in ids]


            if request.method == 'POST' and request.form['search'] != "":
                query = request.form['search']
                #feature_data = current_app.config['DBM'].getLibraryFeatureData()  
                if feature_data == None:
                    feature_data = {}

                #feature_data = current_app.config['MM'].loadNewFeatureData(feature_data, photo_data)
        
                #current_app.config['DBM'].updateLibraryFeatureData(feature_data)          
                images = current_app.config['MM'].searchImages(query, photo_data, feature_data, 5)


    
    return render_template("library.html", session=session,  images=images)

