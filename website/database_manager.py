from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from oauth2client.client import OAuth2Credentials
from oauth2client.client import GoogleCredentials
from flask import flash, session, g
from simple_salesforce import Salesforce, SalesforceLogin
import pandas as pd
from functools import wraps
import json, os

def drive_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' in session and 'drive_credentials' not in session['user']:
            flash('Please login to google drive.', category='error')
        return f(*args, **kwargs)
    return decorated_function

class DatabaseManager:

    def __init__(self, app):
        session_id, instance = SalesforceLogin(username=app.config['DB_USERNAME'], password=app.config['DB_PASSWORD'], security_token=app.config['DB_SECURITY_TOKEN'])
        self.SF = Salesforce(instance=instance, session_id=session_id)

    def connectDrive(self):
        try:
            gauth = GoogleAuth()
            CLIENT_SECRETS = json.loads(os.environ['CLIENT_SECRETS'])
           
            if 'user' in session and 'token' in session['user']:
                token_info = session['user']['token']
                credentials = GoogleCredentials(
                    access_token=token_info['access_token'],
                    client_id=CLIENT_SECRETS['web']['client_id'],
                    client_secret=CLIENT_SECRETS['web']['client_secret'],
                    refresh_token=token_info['refresh_token'],
                    token_expiry=None,
                    token_uri='https://oauth2.googleapis.com/token',
                    user_agent=None,
                    revoke_uri=None
                )
                gauth.credentials = credentials
            
            drive = GoogleDrive(gauth)
            return drive
        except Exception as e:
            print(f"Error in connectDrive: {e}")
            return None


    def createFile(self, text):
        drive = self.connectDrive()
        if drive:
            file1 = drive.CreateFile()
            file1.SetContentString(text)
            file1.Upload({"convert": True})
        else:
            print("Failed to connect to Google Drive or create a file.")
        

