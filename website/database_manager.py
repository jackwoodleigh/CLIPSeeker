from flask import flash, session, g, current_app
from simple_salesforce import Salesforce, SalesforceLogin
import pandas as pd
from functools import wraps
import json, os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from io import StringIO
import time


def drive_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' in session and 'drive_credentials' not in session['user']:
            flash('Please login to google drive.', category='error')
        return f(*args, **kwargs)
    return decorated_function

class DatabaseManager:

    def __init__(self, app):
        session_id, instance = SalesforceLogin(username=app.config['SF_SECRETS']['username'], password=app.config['SF_SECRETS']['password'], security_token=app.config['SF_SECRETS']['security_token'])
        self.SF = Salesforce(instance=instance, session_id=session_id)

    def connectDrive(self):
        try:
            if 'token' in session:
                credentials = Credentials(
                    token=session['token'].get('access_token'),
                    refresh_token=session['token'].get('refresh_token'),
                    token_uri='https://oauth2.googleapis.com/token',
                    client_id=current_app.config['CLIENT_SECRETS']['web']['client_id'],
                    client_secret=current_app.config['CLIENT_SECRETS']['web']['client_secret'])
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

    '''def createFile(self, text):
        drive_service = self.connectDrive()
        if drive_service:
            file_metadata = {'name': 'My Document', 'mimeType': 'application/vnd.google-apps.document'}
            media = MediaIoBaseUpload(StringIO(text), mimetype='text/plain')
            file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        else:
            print("Failed to connect to Google Drive or create a file.")'''
    
    def retrievePhotos(self):
        try:
            credentials = None
            if 'token' in session:
                credentials = Credentials(
                    token=session['token'].get('access_token'),
                    refresh_token=session['token'].get('refresh_token'),
                    token_uri='https://oauth2.googleapis.com/token',
                    client_id=current_app.config['CLIENT_SECRETS']['web']['client_id'],
                    client_secret=current_app.config['CLIENT_SECRETS']['web']['client_secret']
                )

                if credentials and credentials.expired and credentials.refresh_token:
                    credentials.refresh(Request())

            if not credentials or not credentials.valid:
                print("Credentials are not valid or unavailable.")
                return []

            photos_service = build('photoslibrary', 'v1', credentials=credentials, static_discovery=False)

            results = photos_service.mediaItems().list(pageSize=100).execute()
            items = results.get('mediaItems', [])
            all_photos = []
            while 'nextPageToken' in results:
                page_token = results['nextPageToken']
                results = photos_service.mediaItems().list(pageSize=100, pageToken=page_token).execute()
                items.extend(results.get('mediaItems', []))
                if 'nextPageToken' not in results:
                    break

            for item in items:
                all_photos.append({
                    'id': item['id'],
                    'baseUrl': item['baseUrl'],  # Use 'baseUrl' to get the image URL
                    'mimeType': item.get('mimeType', 'image/jpeg'),  # mimeType might not be present
                    'filename': item.get('filename', 'Unnamed')  # Some items might not have a filename
                })

            return all_photos
        except Exception as e:
            print(f"Error in retrievePhotos: {e}")
            return []




        

