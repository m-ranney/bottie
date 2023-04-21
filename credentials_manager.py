import os
import json
from google.oauth2.credentials import Credentials

credentials_json = {
    "token": "ya29.a0Ael9sCNfu-I86M3oCBtYcMXEdakNvkNdG4Syge8hPBUGCSdo-vRsIDPfeCkZy-Q6lAlhhl_4sN_56GU8muokQVyTI9m-",
    "refresh_token": "None",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_id": "143793044167-c48ki99ihdf2kh0ma4l1546nfe4prcb2.apps.googleusercontent.com",
    "client_secret": "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",
    "scopes": ["https://www.googleapis.com/auth/calendar"],
    "expiry": "2023-04-21T23:38:57"
}

os.environ["STORED_CREDENTIALS_JSON"] = json.dumps(credentials_json)

def load_credentials():
    credentials_json = json.loads(os.environ['STORED_CREDENTIALS_JSON'])
    credentials = Credentials.from_authorized_user_info(info=credentials_json)
    return credentials

def save_credentials(credentials):
    credentials_json = json.dumps(credentials.to_json())
    os.environ['STORED_CREDENTIALS_JSON'] = credentials_json

