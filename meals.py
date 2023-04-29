from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import openai
import os
import json
from supabase_py import create_client, Client
from typing import List, Dict
from asyncio import get_event_loop

meal_plan_bp = Blueprint('meal_plan_bp', __name__)

# Initialize Supabase client
supabase_url = os.environ['SUPABASE_URL']
supabase_key = os.environ['SUPABASE_KEY']
supabase: Client = create_client(supabase_url, supabase_key)

# Configure OpenAI API
openai.api_key = os.environ['OPENAI_API_KEY_CE']

# Calls meal plan input from forms on meal_plan.html
@meal_plan_bp.route('/meal_plan', methods=['GET', 'POST'])
def meal_plan():
    if request.method == 'POST':
        num_days = request.form.get('num_days')
        meal_goal = request.form.get('meal_goal')
        response = generate_meal_plan(num_days, meal_goal)
        meal_plan_json = response.get('choices')[0].get('text')
        return render_template('meal_plan.html', meal_plan_json=meal_plan_json)
    return render_template('meal_plan.html')

def generate_meal_plan(num_days, meal_goal):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Please provide a meal plan for {num_days} days, with a focus on {meal_goal} meals. For each day, suggest breakfast, lunch, and dinner options. Be as descriptive as possible and return your response in a bulleted list format.",
        temperature=0.7,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        n=1,
    )
    return response
