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
        meal_plan_text = response.get('choices')[0].get('text').strip()
        meal_plan_dict = meal_plan_to_dict(meal_plan_text)
    return render_template('meal_plan.html', meal_plan_dict=meal_plan_dict)

def generate_meal_plan(num_days, meal_goal):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Please provide a meal plan for {num_days} days, with a focus on {meal_goal} meals. Suggest breakfast, lunch, and dinner options. Be as descriptive as possible. Return your response in the following format: 'Breakfast: Day 1 Meal. Day 2 Meal. Day 3 Meal. etc... Lunch: Day 1 Meal. Day 2 Meal  Day 3 Meal. etc... Dinner: Day 1 Meal. Day 2 Meal. Day 3 Meal. etc...'. Add some variety to the meal suggestions. Apply the ability to buy ingredients that can be used in multiple selected dishes for more efficient grocery shopping.",
        temperature=1,
        max_tokens=400,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        n=1,
    )
    return response

def meal_plan_to_dict(meal_plan_text):
    lines = meal_plan_text.split('\n')
    meal_plan_dict = {}
    current_meal_type = None

    for line in lines:
        if not line:
            continue
        if line.endswith(':'):
            current_meal_type = line[:-1]
            meal_plan_dict[current_meal_type] = []
        elif current_meal_type is not None:
            meal_plan_dict[current_meal_type].append(line)

    return meal_plan_dict


