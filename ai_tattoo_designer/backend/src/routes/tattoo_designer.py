from flask import Blueprint, request, jsonify
from datetime import datetime
import random
import os

tattoo_bp = Blueprint("tattoo_bp", __name__)

def get_zodiac_sign(day, month):
    if (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "Aquarius"
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
        return "Pisces"
    elif (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "Aries"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "Taurus"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "Gemini"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "Cancer"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "Leo"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "Virgo"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "Libra"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "Scorpio"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "Sagittarius"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "Capricorn"

def calculate_life_path_number(dob):
    dob_sum = sum(int(digit) for digit in dob.replace("/", ""))
    while dob_sum > 9:
        dob_sum = sum(int(digit) for digit in str(dob_sum))
    return dob_sum

@tattoo_bp.route("/generate_tattoo", methods=["POST"])
def generate_tattoo():
    data = request.get_json()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    date_of_birth = data.get("date_of_birth")
    age = data.get("age")

    if not isinstance(first_name, str) or not first_name.strip():
        return jsonify({"error": "First name must be a non-empty string"}), 400
    if not isinstance(last_name, str) or not last_name.strip():
        return jsonify({"error": "Last name must be a non-empty string"}), 400
    if not isinstance(age, int) or age <= 0:
        return jsonify({"error": "Age must be a positive integer"}), 400
    if not date_of_birth:
        return jsonify({"error": "Missing input data"}), 400

    try:
        day, month, year = map(int, date_of_birth.split("/"))
        dob_date = datetime(year, month, day)
    except ValueError:
        return jsonify({"error": "Invalid date of birth format. Use dd/mm/yyyy"}), 400

    zodiac_sign = get_zodiac_sign(day, month)
    life_path_number = calculate_life_path_number(date_of_birth)

    symbolic_analysis = f"The name \'{first_name} {last_name}\' vibrates with the energy of Life Path {life_path_number}. Born under {zodiac_sign}, your age of {age} years signifies a period of profound growth and self-discovery."

    core_tattoo_theme = random.choice([
        "Embracing the journey of self-discovery and inner wisdom.",
        "The harmonious balance between strength and serenity.",
        "Unleashing your true potential and embracing transformation.",
        "Connecting with ancestral roots and spiritual guidance."
    ])

    visual_motif_description = random.choice([
        "A celestial compass intertwined with blooming lotus flowers, guiding your path.",
        "A majestic lion with a crown of stars, symbolizing courage and destiny.",
        "An ancient tree with roots reaching deep into the earth and branches touching the cosmos, representing growth and connection.",
        "A flowing river transforming into a dragon, embodying change and power."
    ])

    placement_suggestion = random.choice([
        "Inner forearm, a constant reminder of your inner strength.",
        "Upper back, symbolizing the burdens you've overcome and the freedom you've gained.",
        "Ankle, representing your journey and the steps you take towards your destiny.",
        "Chest, close to your heart, a symbol of your deepest desires and passions."
    ])

    mystical_insight = random.choice([
        "Your destiny is woven in the stars, and your spirit is a beacon of light.",
        "Embrace the whispers of your soul, for they guide you to your true purpose.",
        "The universe conspires in your favor; trust the magic within you.",
        "Every step you take is a dance with destiny; let your heart lead the way."
    ])

    image_prompt = f"A tattoo design featuring {visual_motif_description.lower()}, in a mystical, tarot-inspired style."
    
    # For demo purposes, we'll use a pre-generated image
    image_url = f"http://localhost:5000/static/generated_images/tattoo_john_doe.png"

    return jsonify({
        "symbolic_analysis": symbolic_analysis,
        "core_tattoo_theme": core_tattoo_theme,
        "visual_motif_description": visual_motif_description,
        "placement_suggestion": placement_suggestion,
        "mystical_insight": mystical_insight,
        "image_prompt": image_prompt,
        "image_url": image_url
    })

