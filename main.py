from flask import Flask, render_template, session
from google_calendar import create_oauth_flow, calendar_bp
from steps import steps_bp
from meals import meal_plan_bp
import os
import openai

app = Flask(__name__)
app.register_blueprint(calendar_bp, url_prefix='/calendar')
app.register_blueprint(steps_bp, url_prefix='/steps')
app.register_blueprint(meal_plan_bp, url_prefix='/meal_plan')
app.secret_key = os.environ['FLASK_SECRET_KEY']

# Configure OpenAI API
openai.api_key = os.environ['OPENAI_API_KEY_CE']

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

# Route to the Meal Plan page
@app.route('/meal_plan')
def meal_plan():
    return render_template('meal_plan.html')

#Generate output on homepage chat
def generate_output(input_text):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f" {input_text}",
        temperature=0.7,
        max_tokens=200,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        n=1,
    )
    return response

@app.route("/generate", methods=["POST"])
def generate():
    input_text = request.form.get("input-text")
    response = generate_output(input_text)
    return jsonify({"output": response.choices[0].text})


if __name__ == '__main__':
    app.run(debug=True)
