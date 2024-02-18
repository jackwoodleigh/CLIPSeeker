from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    
    return render_template("login.html", text="test", bool=False)

@auth.route('/logout')
def logout():
    return "<p>logout</p>"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email must be at least 4 characters', category='error') #cat can be anything
        elif len(username) < 2:
            flash('Username must be at least 2 characters', category='error') 
        elif password1 != password2:
            flash('Passwords don\'t match', category='error') 
        elif len(password1) < 4:
            flash('Password must be at least 4 characters', category='error') 
        else:
            flash('Account sucessfully created!', category='success')

    return render_template("sign_up.html")
