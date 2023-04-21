import os
import json
from google.oauth2.credentials import Credentials


def load_credentials():
    credentials_json = json.loads(os.environ['STORED_CREDENTIALS_JSON'])
    credentials = Credentials.from_authorized_user_info(info=credentials_json)
    return credentials

def save_credentials(credentials):
    credentials_json = json.dumps(credentials.to_json())
    os.environ['STORED_CREDENTIALS_JSON'] = credentials_json

