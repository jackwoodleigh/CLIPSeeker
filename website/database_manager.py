from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from oauth2client.client import OAuth2Credentials
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
                credentials = OAuth2Credentials(
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

    '''def connectDrive(self):
        try:

            CLIENT_SECRETS = json.loads(os.environ['CLIENT_SECRETS'])
            gauth = GoogleAuth()
            print(CLIENT_SECRETS)
            gauth.client_config['client_id'] = CLIENT_SECRETS['web']['client_id']
            gauth.client_config['client_secret'] = CLIENT_SECRETS['web']['client_secret']
            gauth.client_config['redirect_uri'] = CLIENT_SECRETS['web']['redirect_uris'][0]

            if 'user' in session and 'drive_credentials' in session['user']:
                gauth.credentials = OAuth2Credentials.from_json(session['user']['drive_credentials'])

                if gauth.credentials is None or gauth.access_token_expired:
                    gauth.LocalWebserverAuth()
                    session['user']['drive_credentials'] = gauth.credentials.to_json()
            else:
                gauth.LocalWebserverAuth()
                session['user']['drive_credentials'] = gauth.credentials.to_json()

            return GoogleDrive(gauth)
        except Exception as e:
            print(f"Error in connectDrive: {e}")
            return None'''

    def createFile(self, text):
        drive = self.connectDrive()
        if drive:
            file1 = drive.CreateFile()
            file1.SetContentString(text)
            file1.Upload({"convert": True})
        else:
            print("Failed to connect to Google Drive or create a file.")
        



'''
  
 <script type="text/javascript">
        document.getElementById('googleLogin').onclick = function() {
            var width = 800, height = 600;
            var left = (screen.width - width) / 2;
            var top = (screen.height - height) / 2;
            var url = "/drive-login"; 
            var opts = `width=${width},height=${height},top=${top},left=${left}`;
            window.open(url, 'googleLogin', opts);
        };
    </script>


app.config['SF'] =   

# Authenticate the client.
gauth = GoogleAuth()
drive = GoogleDrive(gauth)

# Create a file, set content, and upload.
file1 = drive.CreateFile()
original_file_content = "Generic, non-exhaustive\n ASCII test string."
file1.SetContentString(original_file_content)
# {'convert': True} triggers conversion to a Google Drive document.
file1.Upload({"convert": True})


# Download the file.
file2 = drive.CreateFile({"id": file1["id"]})

# Print content before download.
print("Original text:")
print(bytes(original_file_content.encode("unicode-escape")))
print("Number of chars: %d" % len(original_file_content))
print("")
#     Original text:
#     Generic, non-exhaustive\n ASCII test string.
#     Number of chars: 43


# Download document as text file WITH the BOM and print the contents.
content_with_bom = file2.GetContentString(mimetype="text/plain")
print("Content with BOM:")
print(bytes(content_with_bom.encode("unicode-escape")))
print("Number of chars: %d" % len(content_with_bom))
print("")
#     Content with BOM:
#     \ufeffGeneric, non-exhaustive\r\n ASCII test string.
#     Number of chars: 45


# Download document as text file WITHOUT the BOM and print the contents.
content_without_bom = file2.GetContentString(
    mimetype="text/plain", remove_bom=True
)
print("Content without BOM:")
print(bytes(content_without_bom.encode("unicode-escape")))
print("Number of chars: %d" % len(content_without_bom))
print("")
#     Content without BOM:
#     Generic, non-exhaustive\r\n ASCII test string.
#     Number of chars: 44

# *NOTE*: When downloading a Google Drive document as text file, line-endings
# are converted to the Windows-style: \r\n.

'''