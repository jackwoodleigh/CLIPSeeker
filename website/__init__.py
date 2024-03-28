from flask import Flask, g
from flask_login import LoginManager
from .views import views
from .auth import auth
from .database_manager import DatabaseManager
import pandas as pd
import json, os

def create_app():
    app = Flask(__name__)
    DEVELOPMENT = False
    app.config.from_object('config.Config')

    if(DEVELOPMENT):
        app.config['CLIENT_SECRETS'] = json.load(open('client_secrets.json'))
    else:
        app.config['CLIENT_SECRETS'] = json.loads(os.environ['CLIENT_SECRETS'])


    
    app.config['DBM'] = DatabaseManager(app)
  
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    #from .models import User, Note

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







'''
db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dfhgfgshasksdfdghfdhfhd'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')
'''