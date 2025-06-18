import requests
import os
import uuid
import time
import base64
from io import BytesIO
from flask import Blueprint, request, jsonify
from datetime import datetime
import openai
import json

tattoo_bp = Blueprint("tattoo_bp", __name__)

# Initialize OpenAI client
openai.api_key = os.getenv('OPENAI_API_KEY')

# OpenRouter configuration
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Alternative image generation APIs
STABILITY_API_KEY = os.getenv('STABILITY_API_KEY')
REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN') # Ensure this is loaded

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

def generate_tattoo_reading_with_openrouter(first_name, last_name, date_of_birth, age, zodiac_sign, life_path_number):
    """Generate a unique tattoo reading using OpenRouter as backup"""
    
    prompt = f"""
    You are a mystical AI tattoo oracle designer, inspired by tarot reading and symbolic divination. Your task is to create a unique, meaningful tattoo design concept based on the following information:
    
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
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "https://ai-tat-oracle-frontend.onrender.com",
            "X-Title": "AI Tattoo Oracle Designer",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "anthropic/claude-3.5-sonnet",
            "messages": [
                {"role": "system", "content": "You are a mystical AI tattoo oracle designer. Always respond with valid JSON format."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1000,
            "temperature": 0.8
        }
        
        response = requests.post(
            f"{OPENROUTER_BASE_URL}/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        else:
            print(f"OpenRouter API error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Error generating OpenRouter response: {e}")
        return None

def generate_tattoo_reading_with_chatgpt(first_name, last_name, date_of_birth, age, zodiac_sign, life_path_number):
    """Generate a unique tattoo reading using ChatGPT (primary)"""
    
    prompt = f"""
    You are a mystical AI tattoo oracle designer, inspired by tarot reading and symbolic divination. Your task is to create a unique, meaningful tattoo design concept based on the following information:
    
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

def generate_tattoo_reading_with_fallback(first_name, last_name, date_of_birth, age, zodiac_sign, life_path_number):
    """Generate tattoo reading with ChatGPT primary and OpenRouter fallback"""
    
    # Try ChatGPT first
    if openai.api_key:
        chatgpt_response = generate_tattoo_reading_with_chatgpt(
            first_name, last_name, date_of_birth, age, zodiac_sign, life_path_number
        )
        if chatgpt_response:
            return chatgpt_response, "chatgpt"
    
    # Fallback to OpenRouter
    if OPENROUTER_API_KEY:
        openrouter_response = generate_tattoo_reading_with_openrouter(
            first_name, last_name, date_of_birth, age, zodiac_sign, life_path_number
        )
        if openrouter_response:
            return openrouter_response, "openrouter"
    
    # If both fail, return None
    return None, "none"

def generate_image_with_dalle(image_prompt, first_name, last_name):
    """Generate image using DALL-E (OpenAI)"""
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
        print(f"Error generating image with DALL-E: {e}")
        return None

def generate_image_with_stability(image_prompt, first_name, last_name):
    """Generate image using Stability AI"""
    
    if not STABILITY_API_KEY:
        return None
    
    url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {STABILITY_API_KEY}"
    }
    
    payload = {
        "text_prompts": [
            {
                "text": f"{image_prompt} - black and white tattoo design, detailed line art, mystical style",
                "weight": 1
            }
        ],
        "cfg_scale": 7,
        "height": 512,
        "width": 512,
        "samples": 1,
        "steps": 30,
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            
            # Save the image
            unique_id = str(uuid.uuid4())[:8]
            filename = f"tattoo_{first_name}_{last_name}_{unique_id}.png"
            filepath = os.path.join("src/static/generated_images", filename)
            
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Decode and save the base64 image
            image_data = base64.b64decode(data["artifacts"][0]["base64"])
            with open(filepath, 'wb') as f:
                f.write(image_data)
            
            return f"/static/generated_images/{filename}"
            
    except Exception as e:
        print(f"Error generating image with Stability AI: {e}")
        return None

def generate_image_with_replicate(image_prompt, first_name, last_name):
    """Generate image using Replicate"""
    
    api_key = os.getenv("REPLICATE_API_TOKEN")
    if not api_key:
        print("REPLICATE_API_TOKEN not set.")
        return None
    
    headers = {
        "Authorization": f"Token {api_key}",
        "Content-Type": "application/json"
    }
    
    # The specific model and version to use
    model_version = "windxtech/tattoo-generator:0fe0fd450695b2fd99305d27a07ee6349943c200dc849d07633a98c24daef9a8" [cite: 45]
    
    payload = {
        "version": model_version, [cite: 42]
        "input": {
            "prompt": f"{image_prompt} - black and white tattoo design, detailed line art, mystical style",
            "width": 512,
            "height": 512,
            "num_outputs": 1
        }
    }
    
    try:
        # Start the prediction
        start_response = requests.post(
            "https://api.replicate.com/v1/predictions",
            headers=headers,
            json=payload
        )
        start_response.raise_for_status() # Raise an exception for HTTP errors
        prediction_data = start_response.json()
        
        prediction_id = prediction_data["id"]
        
        # Poll for the result
        while True:
            get_response = requests.get(
                f"https://api.replicate.com/v1/predictions/{prediction_id}",
                headers=headers
            )
            get_response.raise_for_status()
            prediction_status = get_response.json()
            
            if prediction_status["status"] == "succeeded": [cite: 59]
                image_url = prediction_status["output"][0] [cite: 54]
                
                # Download and save the image
                image_response = requests.get(image_url)
                image_response.raise_for_status()
                
                unique_id = str(uuid.uuid4())[:8] [cite: 55]
                filename = f"tattoo_{first_name}_{last_name}_{unique_id}.png" [cite: 55]
                filepath = os.path.join("src/static/generated_images", filename) [cite: 55]
                
                os.makedirs(os.path.dirname(filepath), exist_ok=True) [cite: 55]
                with open(filepath, 'wb') as f: [cite: 56]
                    f.write(image_response.content) [cite: 56]
                
                return f"/static/generated_images/{filename}"
            elif prediction_status["status"] == "failed": [cite: 59]
                print(f"Replicate prediction failed: {prediction_status.get('error', 'Unknown error')}") [cite: 57]
                return None
            elif prediction_status["status"] in ["starting", "processing", "queued"]: [cite: 57]
                import time
                time.sleep(2) # Wait for 2 seconds before polling again 
            else:
                print(f"Unexpected Replicate status: {prediction_status['status']}") [cite: 58]
                return None

    except requests.exceptions.RequestException as req_err: [cite: 58]
        print(f"Network or HTTP error with Replicate: {req_err}") [cite: 58]
        return None
    except Exception as e: [cite: 58]
        print(f"Error generating image with Replicate: {e}") [cite: 58]
        return None

def generate_placeholder_image(first_name, last_name):
    """Generate a placeholder when all image services fail"""
    # You could create a simple text-based image or use a default image
    # For now, return None to indicate no image available
    return None

def generate_tattoo_image_with_complete_fallback(image_prompt, first_name, last_name):
    """Try multiple image generation services in order"""
    
    # 1. Try DALL-E (OpenAI)
    if openai.api_key: [cite: 24]
        image_path = generate_image_with_dalle(image_prompt, first_name, last_name) [cite: 24]
        if image_path:
            return image_path, "dalle" [cite: 24]
    
    # 2. Try Stability AI
    if STABILITY_API_KEY: [cite: 28]
        image_path = generate_image_with_stability(image_prompt, first_name, last_name) [cite: 28]
        if image_path:
            return image_path, "stability" [cite: 28]

    # 3. Try Replicate 
    if REPLICATE_API_TOKEN: [cite: 49]
        image_path = generate_image_with_replicate(image_prompt, first_name, last_name) [cite: 49]
        if image_path:
            return image_path, "replicate" [cite: 49]
    
    # 4. Fallback to placeholder or no image
    return generate_placeholder_image(first_name, last_name), "placeholder"

@tattoo_bp.route("/generate_tattoo", methods=["POST"])
def generate_tattoo():
    data = request.get_json()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    date_of_birth = data.get("date_of_birth")
    age = data.get("age")

    # Validation
    if not isinstance(first_name, str) or not first_name.strip(): [cite: 34]
        return jsonify({"error": "First name must be a non-empty string"}), 400
    if not isinstance(last_name, str) or not last_name.strip(): [cite: 35]
        return jsonify({"error": "Last name must be a non-empty string"}), 400
    if not isinstance(age, int) or age <= 0: [cite: 35]
        return jsonify({"error": "Age must be a positive integer"}), 400
    if not date_of_birth: [cite: 35]
        return jsonify({"error": "Missing input data"}), 400

    try:
        day, month, year = map(int, date_of_birth.split("/")) [cite: 35]
        dob_date = datetime(year, month, day) [cite: 35]
    except ValueError: [cite: 36]
        return jsonify({"error": "Invalid date of birth format. Use dd/mm/yyyy"}), 400 [cite: 37]

    # Calculate astrological data
    zodiac_sign = get_zodiac_sign(day, month) [cite: 1, 2, 3, 4]
    life_path_number = calculate_life_path_number(date_of_birth) [cite: 4, 5]

    # Generate unique reading with fallback system
    ai_response, text_provider = generate_tattoo_reading_with_fallback( [cite: 22]
        first_name, last_name, date_of_birth, age, zodiac_sign, life_path_number
    )
    
    if not ai_response:
        return jsonify({"error": "Failed to generate tattoo reading - all AI services unavailable"}), 500
    
    try:
        reading_data = json.loads(ai_response) [cite: 38]
    except json.JSONDecodeError: [cite: 38]
        return jsonify({"error": "Invalid response format from AI"}), 500 [cite: 38]
    
    # Generate image based on the AI's description with complete fallback
    image_path, image_provider = generate_tattoo_image_with_complete_fallback( [cite: 33]
        reading_data.get("image_prompt", ""), first_name, last_name
    )
    
    # Prepare response
    response_data = {
        "symbolic_analysis": reading_data.get("symbolic_analysis", ""), [cite: 39]
        "core_tattoo_theme": reading_data.get("core_tattoo_theme", ""), [cite: 39]
        "visual_motif_description": reading_data.get("visual_motif_description", ""), [cite: 39]
        "placement_suggestion": reading_data.get("placement_suggestion", ""), [cite: 39]
        "mystical_insight": reading_data.get("mystical_insight", ""), [cite: 39]
        "image_prompt": reading_data.get("image_prompt", ""), [cite: 39]
        "image_url": image_path if image_path else None, [cite: 39]
        "ai_provider": f"text:{text_provider},image:{image_provider}"  # For debugging/monitoring 
    }

    return jsonify(response_data)
