import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from flask import Blueprint, redirect, request, url_for

# Create a Blueprint for the Google Calendar-related routes
calendar_bp = Blueprint('calendar', __name__)


# Load client secrets from the JSON file
CLIENT_SECRETS_FILE = "/home/runner/bottie/client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/calendar']


# Create an OAuth 2.0 flow
def create_oauth_flow():
    flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    flow.redirect_uri = "https://bottie.herokuapp.com/oauth2callback"
    return flow

# Create an authentication route using the Blueprint
@calendar_bp.route('/auth')
def auth():
    flow = create_oauth_flow()
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')
    return redirect(authorization_url)
