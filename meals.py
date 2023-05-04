from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import openai
import os
import json
import re
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
    meal_plan_text = ''
    meal_plan_dict = {}
    if request.method == 'POST':
        meal_goal = request.form.get('meal_goal')
        response = generate_meal_plan(meal_goal)
        meal_plan_text = response['choices'][0]['message']['content'].strip()
        meal_plan_dict = meal_plan_to_dict(meal_plan_text)
    return render_template('meal_plan.html', meal_plan_dict=meal_plan_dict, meal_plan_text=meal_plan_text)

def generate_meal_plan(meal_goal):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides meal plans."},
            {"role": "user", "content": f"Please provide a meal plan with a focus on {meal_goal} meals. Suggest multiple meals for breakfast, lunch, and dinner. Suggest at least 10 meals. Be as descriptive as possible. Include meals using the following format template, with one meal per line, for your response:---BEGIN FORMAT TEMPLATE---(Meal Type): (Meal). (Meal Type): (Meal).---END FORMAT TEMPLATE--- An example is 'Breakfast: Greek yogurt with blueberries and granola. \n Breakfast: Protein bar and a banana with coffee. \n Lunch: Kale salad with roasted chicken, dried cranberries and toasted walnuts. /n Dinner: Grilled salmon with roasted Brussels sprouts and roasted sweet potato.' Add some variety to the meal suggestions. Apply the ability to buy ingredients that can be used in multiple selected dishes for more efficient grocery shopping."}
        ],
        max_tokens=400,
    )
    return response

def meal_plan_to_dict(meal_plan_text):
    meal_plan_dict = {'meals': []}
    pattern = r'(?=(Breakfast|Lunch|Dinner))'
    meal_strings = re.split(pattern, meal_plan_text)

    for i in range(1, len(meal_strings), 2):
        meal_type = meal_strings[i].strip()
        meal = meal_strings[i+1].strip().rstrip('/n')  # Remove spaces and trailing /n from the meal description
        meal_plan_dict['meals'].append({'meal_type': meal_type, 'meal': meal})

    return meal_plan_dict



