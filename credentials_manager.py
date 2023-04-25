import os
import json
from google.oauth2.credentials import Credentials


def load_credentials():
    credentials_json = session.get('stored_credentials')
    if credentials_json:
        credentials = Credentials.from_authorized_user_info(info=credentials_json)
        return credentials
    return None

def save_credentials(credentials):
    credentials_json = json.loads(credentials.to_json())
    session['stored_credentials'] = credentials_json


