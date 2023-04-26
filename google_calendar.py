import os
import json
import openai
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import Flow
from flask import Blueprint, redirect, render_template, request, url_for, session, jsonify
from flask.helpers import make_response
from credentials_manager import load_credentials, save_credentials
from datetime import date

# Create a Blueprint for the Google Calendar-related routes
calendar_bp = Blueprint('calendar', __name__)

# Set up OpenAI API key
openai.api_key = os.environ['OPENAI_API_KEY_CE']

# Load client secrets from the JSON file
SCOPES = ['https://www.googleapis.com/auth/calendar']

# New route to handle form submission and render template of OpenAis output 
@calendar_bp.route('/create_event', methods=['GET', 'POST'])
def create_event():
    event_json = None
    success_message = None
    
    # If the user is not logged in, redirect to the login page
    if request.method == 'POST':
        user_input = request.form['event_input']
        event_json = process_input_with_openai(user_input)

        # Store event_json in session
        session['event_json'] = event_json
      
        # Load the user's credentials
        if os.environ.get("STORED_CREDENTIALS_JSON"):
            credentials = Credentials.from_authorized_user_info(info=json.loads(os.environ["STORED_CREDENTIALS_JSON"]))
        else:
            credentials = load_credentials()
  
        # Debugging: Check if the credentials are not None
        if credentials is None:
            auth_url = url_for('calendar.auth')
            return redirect(auth_url)

        # Debugging: Print credentials to verify they are being retrieved correctly
        print("User credentials: ", credentials)
      
        # Call the create_google_calendar_event function to create the event
        success_message = create_google_calendar_event(event_json, credentials)
  
    return render_template('create_event.html', event_json=event_json, success_message=success_message)


# Process the input from user and process with the OpenAI API
def process_input_with_openai(user_input):

    # Set today to be todays date  
    today = date.today().strftime("%Y%m%d")
    
    # OpenAI prompt to generate event details
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"""Use the information from '{user_input}' to generate an event that can be imported into Google Calendar. Assume that today is {today}. Parse the event date, start time, and duration from the user input, and generate the event details in JSON format: '{{"summary": "Example Event", "start": {{"dateTime": "2023-05-01T09:00:00-07:00", "timeZone": "America/Los_Angeles"}}, "end": {{"dateTime": "2023-05-01T09:00:00-07:00", "timeZone": "America/Los_Angeles"}}}}'.""",
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].text.strip()



# Create an OAuth 2.0 flow
def create_oauth_flow():
    client_secrets = json.loads(os.environ['CLIENT_SECRET_JSON'])
    flow = Flow.from_client_config(client_secrets, SCOPES)
    return flow

# Create an authentication route using the Blueprint
@calendar_bp.route('/auth')
def auth():
    flow = create_oauth_flow()
    flow.redirect_uri = url_for('calendar.callback', _external=True, _scheme='https')
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent')
    response = make_response(redirect(authorization_url))
    response.set_cookie('state', state)
    return response

# Function to handle the callback from Google after the user grants or denies permission
@calendar_bp.route('/callback')
def callback():
    state = request.cookies.get('state')
    flow = create_oauth_flow()
    flow.redirect_uri = url_for('calendar.callback', _external=True, _scheme='https')
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    os.environ["STORED_CREDENTIALS_JSON"] = credentials.to_json() 
    save_credentials(credentials)

    # Retrieve event_json from session and create the event
    event_json = session.get('event_json')
    if event_json:
        success_message = create_google_calendar_event(event_json, credentials)
        return f"Event created: {success_message}"
  
    try:
        # Use the credentials to access the Google Calendar API
        service = build('calendar', 'v3', credentials=credentials)
        calendar = service.calendars().get(calendarId='primary').execute()

        # Get the calendar's name and timezone
        calendar_name = calendar['summary']
        calendar_timezone = calendar['timeZone']

        # Return a simple message with the calendar's name and timezone
        return f"Calendar '{calendar_name}' has timezone: {calendar_timezone}"

    except HttpError as error:
        print(f"An error occurred: {error}")
        return "An error occurred while accessing the Google Calendar API."


# Create an event in google calendar
def create_google_calendar_event(event_json, credentials):
    try:
        from google.oauth2.credentials import Credentials

        user_credentials = Credentials.from_authorized_user_info(info=json.loads(credentials.to_json()))
        service = build('calendar', 'v3', credentials=user_credentials, cache_discovery=False)
        
        event = service.events().insert(calendarId='primary', body=json.loads(event_json)).execute()
        return f"Event created: {event['htmlLink']}"

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None
