from flask import flash, session, g, current_app, redirect, url_for
from simple_salesforce import Salesforce, SalesforceLogin
import pandas as pd
from functools import wraps
import json, os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload
import time, io
import torch


def drive_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'token' not in session['user']:
            flash('Please login to google drive.', category='error')
        return f(*args, **kwargs)
    return decorated_function

class DatabaseManager:

    def __init__(self, app):
        session_id, instance = SalesforceLogin(username=app.config['SF_SECRETS']['username'], password=app.config['SF_SECRETS']['password'], security_token=app.config['SF_SECRETS']['security_token'])
        self.SF = Salesforce(instance=instance, session_id=session_id)

    def connectDrive(self):
        try:
            credentials = self.getCredential()
            drive_service = build('drive', 'v3', credentials=credentials)
            return drive_service
        except Exception as e:
            print(f"Error in connectDrive: {e}")
            return None
        

    def getCredential(self):
        if 'token' in session:
            credentials = Credentials(
                token=session['token'].get('access_token'),
                refresh_token=session['token'].get('refresh_token'),
                token_uri='https://oauth2.googleapis.com/token',
                client_id=current_app.config['CLIENT_SECRETS']['web']['client_id'],
                client_secret=current_app.config['CLIENT_SECRETS']['web']['client_secret']
            )

            if credentials.expired and credentials.refresh_token:
                try:
                    #credentials.refresh(Request())
                    request = Request()
                    credentials.refresh(request)
                    session['token'] = {
                        'access_token': credentials.token,
                        'refresh_token': credentials.refresh_token
                    }
                    credentials = Credentials(
                        token=session['token'].get('access_token'),
                        refresh_token=session['token'].get('refresh_token'),
                        token_uri='https://oauth2.googleapis.com/token',
                        client_id=current_app.config['CLIENT_SECRETS']['web']['client_id'],
                        client_secret=current_app.config['CLIENT_SECRETS']['web']['client_secret']
                    )
                except Exception as e:
                    print("Failed to refresh token.")
                    session.pop('token', None)
                    return None
            
            
            return credentials
        else:
            print(f"Error in getting credentials")
            return None
          
        
        
    def getLibraryFeatureData(self):
        credentials = self.getCredential()
        if credentials is None:
            return None
        service = build('drive', 'v3', credentials=credentials)
        filename = 'CLIPbrarian_data.json'
        file_id = self.getFileIdByName(service, filename)

        
        file_id = self.getFileIdByName(service, filename)
        
        if not file_id:
            print(f"File '{file_id}' does not exist in Google Drive.")
            return None

        # downloading library data from drive
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        
        done = False
        while not done:
            status, done = downloader.next_chunk()

        fh.seek(0)
        json_data = fh.read().decode('utf-8')
        data_dict = json.loads(json_data)
        tensor_dict = {}
        for key, value in data_dict.items():
            tensor_dict[key] = torch.tensor(value, dtype=torch.float)

        return tensor_dict
        
    def updateLibraryFeatureData(self, data):
        credentials = self.getCredential()
        if credentials is None:
            return None
        service = build('drive', 'v3', credentials=credentials)
        

        filename = 'CLIPbrarian_data.json'
        file_id = self.getFileIdByName(service, filename)

        serializable_data = {}
        for key, value in data.items():
            serializable_data[key] = [i.tolist() for i in value]
          

        data = json.dumps(serializable_data)
        fh = io.BytesIO(data.encode('utf-8'))
        media = MediaIoBaseUpload(fh, mimetype='application/json')

        # checking if the file is in the drive
        '''if file_id:
            updated_file = service.files().update(
                fileId=file_id,
                media_body=media
            ).execute()
            print(f"Updated existing file '{filename}' with ID {updated_file.get('id')}.")

        # if the file does not exist, create a new file
        else:'''
        file_metadata = {'name': filename}
        new_file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        print(f"Created new file '{filename}' with ID {new_file.get('id')}.")


    def deleteLibraryFeatureData(self):
        credentials = self.getCredential()
        if credentials is None:
            return None
        service = build('drive', 'v3', credentials=credentials)
        filename = 'CLIPbrarian_data.json'
        file_id = self.getFileIdByName(service, filename)

        
        file_id = self.getFileIdByName(service, filename)
        
        if not file_id:
            print(f"File '{file_id}' does not exist in Google Drive.")
            return None

        try:
            # Attempt to delete the file from Google Drive
            service.files().delete(fileId=file_id).execute()
            print(f"File '{filename}' has been successfully deleted from Google Drive.")
        except Exception as e:
            # Handle exceptions, such as permission errors or network issues
            print(f"An error occurred: {e}")
            return None

        return True
       


    def getFileIdByName(self, service, filename):
        query = f"name = '{filename}'"
        response = service.files().list(q=query, fields="files(id)").execute()
        files = response.get('files', [])
        return files[0].get('id') if files else None
 
    def loadFileIdsToSession(self):
        feature_data = self.getLibraryFeatureData()  
        if feature_data != None:
            session['fileids'] = True
            return list(feature_data.keys()), feature_data
        else:
            session['fileids'] = False
            return [], []


    def retrievePhotos(self):
        try:
            credentials = self.getCredential()
            photos_service = build('photoslibrary', 'v1', credentials=credentials, static_discovery=False)
            results = photos_service.mediaItems().list(pageSize=100).execute()

            items = results.get('mediaItems', [])
            all_photos = {}
            while 'nextPageToken' in results:
                page_token = results['nextPageToken']
                results = photos_service.mediaItems().list(pageSize=100, pageToken=page_token).execute()
                items.extend(results.get('mediaItems', []))
                if 'nextPageToken' not in results:
                    break

            for item in items:
                all_photos[item['id']] = item['baseUrl']
                '''all_photos.append({
                    'id': item['id'],
                    'baseUrl': item['baseUrl'], 
                    'mimeType': item.get('mimeType', 'image/jpeg'), 
                    'filename': item.get('filename', 'Unnamed')  
                })'''

            return all_photos
        except Exception as e:
            print(f"Error in retrievePhotos: {e}")
            return None


    def storeMedia(self, media):
        pass


    '''def createFile(self, text):
        drive_service = self.connectDrive()
        if drive_service:
            file_metadata = {'name': 'My Document', 'mimeType': 'application/vnd.google-apps.document'}
            media = MediaIoBaseUpload(StringIO(text), mimetype='text/plain')
            file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        else:
            print("Failed to connect to Google Drive or create a file.")'''
    