from flask import Blueprint, request, jsonify
from datetime import datetime
import os
import openai
import uuid
import requests
from io import BytesIO
import base64

tattoo_bp = Blueprint("tattoo_bp", __name__)

# Initialize OpenAI client
openai.api_key = os.getenv('OPENAI_API_KEY')

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

def generate_tattoo_reading_with_chatgpt(first_name, last_name, date_of_birth, age, zodiac_sign, life_path_number):
    """Generate a unique tattoo reading using ChatGPT"""
    
    prompt = f"""
    You are a mystical AI tattoo oracle designer, inspired by tarot reading and symbolic divination. 
    Your task is to create a unique, meaningful tattoo design concept based on the following information:
    
    - First Name: {first_name}
    - Last Name: {last_name}
    - Date of Birth: {date_of_birth}
    - Age: {age}
    - Zodiac Sign: {zodiac_sign}
    - Life Path Number: {life_path_number}
    
    Please provide your response in the following JSON format:
    {{
        "symbolic_analysis": "Interpret name numerology, zodiac sign, and any relevant symbolic meanings derived from DOB and age.",
        "core_tattoo_theme": "Describe the emotional, spiritual, or archetypal essence the tattoo should express.",
        "visual_motif_description": "Provide a vivid, imaginative description of the tattoo's visual elements (symbols, shapes, animals, patterns, etc.).",
        "placement_suggestion": "Recommend ideal body placement and size (e.g., upper forearm, chest, sleeve, ankle).",
        "mystical_insight": "End with a brief fortune-style message tied to the design meaning.",
        "image_prompt": "A detailed prompt for generating the tattoo image, describing the visual elements in a way suitable for AI image generation."
    }}
    
    Style & Tone:
    - Mysterious yet poetic
    - Tarot card reader meets visionary tattoo artist
    - Use rich metaphors and artistic vocabulary
    - Avoid generic or overused symbols—focus on originality and meaningful storytelling
    - Each reading should be completely unique and personalized
    
    Make sure the response is valid JSON and each field contains meaningful, unique content based on the person's specific information.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a mystical AI tattoo oracle designer. Always respond with valid JSON format."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.8
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating ChatGPT response: {e}")
        return None

def generate_tattoo_image(image_prompt, first_name, last_name):
    """Generate a tattoo image using DALL-E"""
    try:
        response = openai.Image.create(
            prompt=f"{image_prompt} - black and white tattoo design, detailed line art, mystical style",
            n=1,
            size="512x512"
        )
        
        image_url = response['data'][0]['url']
        
        # Download and save the image
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            # Create unique filename
            unique_id = str(uuid.uuid4())[:8]
            filename = f"tattoo_{first_name}_{last_name}_{unique_id}.png"
            filepath = os.path.join("src/static/generated_images", filename)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Save image
            with open(filepath, 'wb') as f:
                f.write(image_response.content)
            
            return f"/static/generated_images/{filename}"
        
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

@tattoo_bp.route("/generate_tattoo", methods=["POST"])
def generate_tattoo():
    data = request.get_json()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    date_of_birth = data.get("date_of_birth")
    age = data.get("age")

    # Validation
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

    # Calculate astrological data
    zodiac_sign = get_zodiac_sign(day, month)
    life_path_number = calculate_life_path_number(date_of_birth)

    # Generate unique reading with ChatGPT
    chatgpt_response = generate_tattoo_reading_with_chatgpt(
        first_name, last_name, date_of_birth, age, zodiac_sign, life_path_number
    )
    
    if not chatgpt_response:
        return jsonify({"error": "Failed to generate tattoo reading"}), 500
    
    try:
        import json
        reading_data = json.loads(chatgpt_response)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid response format from AI"}), 500
    
    # Generate image based on the AI's description
    image_path = generate_tattoo_image(reading_data.get("image_prompt", ""), first_name, last_name)
    
    # Prepare response
    response_data = {
        "symbolic_analysis": reading_data.get("symbolic_analysis", ""),
        "core_tattoo_theme": reading_data.get("core_tattoo_theme", ""),
        "visual_motif_description": reading_data.get("visual_motif_description", ""),
        "placement_suggestion": reading_data.get("placement_suggestion", ""),
        "mystical_insight": reading_data.get("mystical_insight", ""),
        "image_prompt": reading_data.get("image_prompt", ""),
        "image_url": image_path if image_path else None
    }

    return jsonify(response_data)


