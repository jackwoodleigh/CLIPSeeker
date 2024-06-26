from flask import Flask, g
from flask_login import LoginManager
from .views import views
from .auth import auth
from .database_manager import DatabaseManager
from .media_manager import MediaManager
import pandas as pd
import json, os

def create_app():
    app = Flask(__name__, static_folder='static')
    DEVELOPMENT = True
    app.config['SECRET_KEY'] = "sdfsdgasdg32y35dfujesf42geasca8fg2vnuwfrg"
    app.config['DEBUG'] = False
    app.config['TESTING'] = False

    if(DEVELOPMENT):
        app.config['CLIENT_SECRETS'] = json.load(open('client_secrets.json'))
        app.config['SF_SECRETS'] = json.load(open('salesforce_secrets.json'))
    else:
        app.config['CLIENT_SECRETS'] = json.loads(os.environ['CLIENT_SECRETS'])
        app.config['SF_SECRETS'] = json.loads(os.environ['SF_SECRETS'])


    
    app.config['DBM'] = DatabaseManager(app)
    app.config['MM'] = MediaManager(app)

  
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        result = app.config['SF'].query_all("SELECT Id, Email__c, FirstName__c, LastName__c, Password__c FROM CLIPAccount__c WHERE Id = '{}'".format(id)).loc[0]
        
        if result['records']:
            result = pd.DataFrame(result['records'])
        # If a user is found, return a dictionary representing the user
            user = result['records'][0]
            return {'id': user['Id'], 'email': user['Email__c'], 'first_name': user['FirstName__c'], 'last_name': user['LastName__c'], 'password': user['Password__c'], }
        else:
            # If no user is found, return None
            return None
        
        #return User.query.get(int(id))

    return app


