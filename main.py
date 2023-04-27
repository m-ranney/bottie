from flask import Flask, render_template, session
from google_calendar import create_oauth_flow, calendar_bp
import os

app = Flask(__name__)
app.register_blueprint(calendar_bp, url_prefix='/calendar')
app.register_blueprint(steps_bp)
app.secret_key = os.environ['FLASK_SECRET_KEY']

# Route to the Home page
@app.route('/')
def home():
    success_message = session.pop('success_message', None)  # Get the success_message from the session and remove it
    event_json = session.pop('event_json', None)  # Get the event_json from the session and remove it
    return render_template('index.html', success_message=success_message, event_json=event_json)


# Route to the Create Event page
@app.route('/create')
def create():
    return render_template('create_event.html')


# Route to the Step by Step page
@app.route('/steps')
def steps():
    return render_template('steps.html')


if __name__ == '__main__':
    app.run(debug=True)
