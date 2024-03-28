from flask import flash, session, g
from simple_salesforce import Salesforce, SalesforceLogin
import pandas as pd
from functools import wraps
import json, os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from io import StringIO



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
            print(session['token'])
            if 'token' in session:
                credentials = Credentials(
                    token=session['token'].get('access_token'),
                    refresh_token=session['token'].get('refresh_token'),
                    token_uri='https://oauth2.googleapis.com/token',
                    client_id=json.loads(os.environ['CLIENT_SECRETS'])['web']['client_id'],
                    client_secret=json.loads(os.environ['CLIENT_SECRETS'])['web']['client_secret'])
            else:
                print("Credentials not in session.")
                return None
            
            if not credentials.valid:
                if credentials.expired and credentials.refresh_token:
                    credentials.refresh(Request())
                else:
                    print("Credentials are not valid and can't be refreshed.")
                    return None

            drive_service = build('drive', 'v3', credentials=credentials)
            return drive_service
        except Exception as e:
            print(f"Error in connectDrive: {e}")
            return None

    def createFile(self, text):
        drive_service = self.connectDrive()
        if drive_service:
            file_metadata = {'name': 'My Document', 'mimeType': 'application/vnd.google-apps.document'}
            media = MediaIoBaseUpload(StringIO(text), mimetype='text/plain')
            file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            print(f"File ID: {file.get('id')}")
        else:
            print("Failed to connect to Google Drive or create a file.")
'''
    def createFile(self, text):
        drive = self.connectDrive()
        if drive:
            file1 = drive.CreateFile()
            file1.SetContentString(text)
            file1.Upload({"convert": True})
        else:
            print("Failed to connect to Google Drive or create a file.")'''
        

