import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from flask import Blueprint, redirect, request, url_for

# Create a Blueprint for the Google Calendar-related routes
calendar_bp = Blueprint('calendar', __name__)

# Load client secrets from the JSON file
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Create an OAuth 2.0 flow
def create_oauth_flow():
    client_secrets = json.loads(os.environ['CLIENT_SECRET_JSON'])
    flow = Flow.from_client_config(client_secrets, SCOPES)
    return flow

# Create an authentication route using the Blueprint
@calendar_bp.route('/auth')
def auth():
    flow = create_oauth_flow()
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')
    return redirect(authorization_url)
