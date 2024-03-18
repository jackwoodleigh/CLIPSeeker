from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from functools import wraps
import pandas as pd

auth = Blueprint('auth', __name__)
def logout_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            flash('Please logout to access this page.', category='success')
            return redirect(url_for('views.home'))
        return f(*args, **kwargs)
    return decorated_function



@auth.route('/login', methods=['GET', 'POST'])
@logout_required
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password1')

        user = current_app.config['SF'].query_all("SELECT Id, Email__c, FirstName__c, LastName__c, Password__c FROM CLIPAccount__c WHERE Email__c = '{}'".format(email))
        
    
        if user['records']:
            user = pd.DataFrame(user['records']).loc[0]
            if check_password_hash(user['Password__c'], password):
                flash('Logged in sucessfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Failed login, try again', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template("login.html", text="test", bool=False, current_user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
@logout_required
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = current_app.config['SF'].query_all("SELECT Email__c FROM CLIPAccount__c WHERE Email__c = '{}'".format(email))
        
        if user['records']:
            flash('Email already Exists', category='error')
        elif len(email) < 4:
            flash('Email must be at least 4 characters', category='error') #cat can be anything
        elif len(username) < 2:
            flash('Username must be at least 2 characters', category='error') 
        elif password1 != password2:
            flash('Passwords don\'t match', category='error') 
        elif len(password1) < 4:
            flash('Password must be at least 4 characters', category='error') 
        else:

            current_app.config['SF'].CLIPAccount__c.create({'Email__c': email, 'FirstName__c': username, 'LastName__c': username, 'Password__c': generate_password_hash(password1)})
            flash('Account sucessfully created!', category='success')
            return redirect(url_for('auth.login'))

    return render_template("sign_up.html", current_user=current_user) 
