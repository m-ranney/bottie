from flask import Flask, render_template
from google_calendar import create_oauth_flow, calendar_bp

app = Flask(__name__)
app.register_blueprint(calendar_bp, url_prefix='/calendar')


@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
