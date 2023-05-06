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
            {"role": "user", "content": f"Please provide a meal plan with a focus on {meal_goal} meals. Suggest at least 10 meals, including multiple meals for breakfast, lunch, and dinner. Be as descriptive as possible, but do not provide recipes or cooking instructions. Use the format template provided and use a single delimiter (newline character '\\n') between each meal.---BEGIN FORMAT TEMPLATE---(Meal Type): (Meal)\\n---END FORMAT TEMPLATE--- For example, 'Breakfast: Greek yogurt with blueberries and granola.\\n Breakfast: Breakfast tacos with eggs, pico de gallo and hot sauce.\\n' Ensure variety in the meal suggestions and the ability to buy ingredients that can be used in multiple selected dishes for efficient grocery shopping."}
        ],
        max_tokens=600,
    )
    return response


def meal_plan_to_dict(meal_plan_text):
    meal_plan_dict = {'meals': []}
    current_meal_type = None

    for line in meal_plan_text.splitlines():
        meal_type_match = re.match(r'^(Breakfast|Lunch|Dinner|Snacks|Dessert):', line.strip())
        if meal_type_match:
            current_meal_type = meal_type_match.group(1)
        else:
            meal_description = re.sub(r'^\W+', '', line.strip())  # Remove extra characters before the meal description
            if meal_description:
                meal_plan_dict['meals'].append({'meal_type': current_meal_type, 'meal': meal_description})

    return meal_plan_dict

