from flask import Flask, render_template, session
from google_calendar import create_oauth_flow, calendar_bp

app = Flask(__name__)
app.register_blueprint(calendar_bp, url_prefix='/calendar')
app.secret_key = os.environ['FLASK_SECRET_KEY']

# Route to the Home page
@app.route('/')
def home():
    return render_template('index.html')

# Route to the Create Event page
@app.route('/create')
def create():
    return render_template('create_event.html')


if __name__ == '__main__':
    app.run(debug=True)
