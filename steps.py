from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import openai
import os
from supabase_py import create_client, Client
from typing import List, Dict

steps_bp = Blueprint('steps_bp', __name__)

# Initialize Supabase client
supabase_url = os.environ['SUPABASE_URL']
supabase_key = os.environ['SUPABASE_KEY']
supabase: Client = create_client(supabase_url, supabase_key)

# Configure OpenAI API
openai.api_key = os.environ['OPENAI_API_KEY_CE']

# Calls task input from form on steps.html
@steps_bp.route('/steps', methods=['GET', 'POST'])
def steps():
    if request.method == 'POST':
        task_input = request.form.get('task_input')
        response = generate_subtasks(task_input)
        subtasks_json = response.get('choices')[0].get('text')
        return render_template('steps.html', subtasks_json=subtasks_json)
    return render_template('steps.html')


def generate_subtasks(task_input):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Please provide a list of detailed subtasks required to complete the task: {task_input}. Be as descriptive as possible and return your response in a bulleted list format. Be creative in your response and in general lean towards using modern technology solutions to make the subtasks as efficient as possible.",
        temperature=0.7,
        max_tokens=200,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        n=1,
    )
    return response




