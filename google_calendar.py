import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow

# Load client secrets from the JSON file
CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Create an OAuth 2.0 flow
def create_oauth_flow():
    flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    flow.redirect_uri = "https://bottie.herokuapp.com/oauth2callback"
    return flow
