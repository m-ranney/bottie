import os
import json
from google.oauth2.credentials import Credentials
from flask import session


def load_credentials():
    if os.environ.get("STORED_CREDENTIALS_JSON"):
        return Credentials.from_authorized_user_info(info=json.loads(os.environ["STORED_CREDENTIALS_JSON"]))
    return None


def save_credentials(credentials):
    credentials_json = json.loads(credentials.to_json())
    session['stored_credentials'] = credentials_json


