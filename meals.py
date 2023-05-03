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
    meal_plan_text = ''
    meal_plan_dict = {}
    if request.method == 'POST':
        num_days = request.form.get('num_days')
        meal_goal = request.form.get('meal_goal')
        response = generate_meal_plan(num_days, meal_goal)
        meal_plan_text = response.get('choices')[0].get('text').strip()
        meal_plan_dict = meal_plan_to_dict(meal_plan_text)
    return render_template('meal_plan.html', meal_plan_dict=meal_plan_dict, meal_plan_text=meal_plan_text)

def generate_meal_plan(num_days, meal_goal):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Please provide a meal plan for {num_days} days, with a focus on {meal_goal} meals. Suggest meals for breakfast, lunch, and dinner. Be as descriptive as possible. Include meals using the following format template, with one meal per line, for your response:---BEGIN FORMAT TEMPLATE---(Day #) - (Meal Type): (Meal). ---END FORMAT TEMPLATE--- An example is 'Day 1 - Breakfast: Greek yogurt with blueberries. \n Day 1 - Lunch: Kale salad with roasted chicken. /n Day 1 - Dinner: Grilled salmon with roasted Brussels sprouts and roasted sweet potato.' Add some variety to the meal suggestions. Apply the ability to buy ingredients that can be used in multiple selected dishes for more efficient grocery shopping.",
        temperature=1,
        max_tokens=400,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        n=1,
    )
    return response

def meal_plan_to_dict(meal_plan_text):
    meal_plan_text = meal_plan_text.replace('/n', '\n')
    lines = meal_plan_text.split('\n')
    meal_plan_dict = {}

    for line in lines:
        if not line:
            continue

        parts = line.split(' - ')
        if len(parts) != 3:
            continue

        day, meal_type, meal = parts
        day = day.strip()

        if day not in meal_plan_dict:
            meal_plan_dict[day] = {}

        meal_type = meal_type.strip()
        meal = meal.strip()

        meal_plan_dict[day][meal_type] = meal

    return meal_plan_dict
