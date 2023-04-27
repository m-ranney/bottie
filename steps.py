from flask import Blueprint, render_template, request, redirect, url_for, jsonify
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
openai.api_key = os.environ['OPENAI_API_KEY_CE']

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
    tasks = supabase.table('tasks').select('*').execute().get('data', [])
    subtasks = supabase.table('subtasks').select('*').execute().get('data', [])
    return render_template('steps.html', tasks=tasks, subtasks=subtasks)

@steps_bp.route('/steps', methods=['POST'])
def add_task():
    task = request.form.get('task')
    subtasks = generate_subtasks(task)

    response = supabase.table('tasks').insert({'task': task}).execute()

    if response.get("status_code") == 201:
        task_id = response["data"][0]["id"]
        for subtask in subtasks:
            supabase.table('subtasks').insert({'task_id': task_id, 'subtask': subtask, 'status': False}).execute()
    else:
        # Handle the error response
        print("Error:", response)

    return redirect(url_for('steps_bp.steps'))

@steps_bp.route('/steps/save', methods=['POST'])
def save_task_and_subtasks():
    data = request.get_json()
    task = data.get('task', '')
    subtasks = data.get('subtasks', [])

    if not task:
        return jsonify({"error": "Task cannot be empty"}), 400

    task_insert = supabase.table('tasks').insert({'task': task}).execute()

    if 'id' not in task_insert['data']:
        return jsonify({"error": "Error saving task"}), 500

    task_id = task_insert['data']['id']

    for subtask in subtasks:
        supabase.table('subtasks').insert({'task_id': task_id, 'subtask': subtask, 'status': False}).execute()

    return jsonify({"message": "Task and subtasks saved successfully"}), 200

@steps_bp.route('/update_status/<int:subtask_id>', methods=['POST'])
def update_status(subtask_id):
    new_status = request.form.get('status') == '1'
    supabase.table('subtasks').update({'status': new_status}).eq('id', subtask_id).execute()
    return redirect(url_for('steps_bp.steps'))

@steps_bp.route('/steps/api/generate_subtasks', methods=['POST'])
def api_generate_subtasks():
    task = request.json.get('task')
    if not task:
        return jsonify({"error": "Task is required"}), 400

    subtasks = generate_subtasks(task)
    return jsonify(subtasks)

