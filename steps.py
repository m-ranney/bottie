from flask import Blueprint, render_template, request, redirect, url_for
import openai
import os
from supabase_py import create_client, Client
from typing import List, Dict

steps_bp = Blueprint('steps_bp', __name__, template_folder='templates')

# Initialize Supabase client
supabase_url = os.environ['SUPABASE_URL']
supabase_key = os.environ['SUPABASE_KEY']
supabase: Client = create_client(supabase_url, supabase_key)

# Configure OpenAI API
openai.api_key = os.environ['OPENAI_API_KEY']

def generate_subtasks(prompt: str) -> List[str]:
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Please provide a list of detailed subtasks required to complete the task: {prompt}. Be as descriptive as possible and return your response in a bulleted list format. Be creative in your response and in general lean towards using modern technology solutions to make the subtasks as efficient as possible.",
        temperature=0.7,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        n=1,
    )

    subtasks_raw = response.choices[0].text.strip()
    subtasks = subtasks_raw.split("\n")
    return [subtask.strip() for subtask in subtasks if subtask.strip()]

@steps_bp.route('/steps', methods=['GET'])
def steps():
    tasks = supabase.table('tasks').select('*').execute()
    return render_template('steps.html', tasks=tasks)

@steps_bp.route('/steps', methods=['POST'])
def add_task():
    task = request.form.get('task')
    subtasks = generate_subtasks(task)

    task_id = supabase.table('tasks').insert({'task': task, 'subtasks': subtasks}).execute()['id']

    return redirect(url_for('steps_bp.steps'))

@steps_bp.route('/update_status/<int:task_id>', methods=['POST'])
def update_status(task_id):
    new_status = request.form.get('status') == '1'
    supabase.table('tasks').update({'status': new_status}).eq('id', task_id).execute()
    return redirect(url_for('steps_bp.steps'))
