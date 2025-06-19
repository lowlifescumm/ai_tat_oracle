from flask import Blueprint, request, jsonify
from datetime import datetime
import os
import openai
import uuid
import requests
from io import BytesIO
import base64
import json

tattoo_bp = Blueprint("tattoo_bp", __name__)

# Initialize OpenAI client
openai.api_key = os.getenv('OPENAI_API_KEY')

# OpenRouter configuration
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Alternative image generation APIs
STABILITY_API_KEY = os.getenv('STABILITY_API_KEY')
REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')

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

def build_enhanced_prompt(first_name, last_name, date_of_birth, age, zodiac_sign, life_path_number, 
                         birthplace=None, favorite_element=None, preferred_aesthetic=None, 
                         spirit_animal=None, life_theme=None, personal_story=None, cultural_affiliation=None):
    """Build an enhanced prompt with additional personalization data"""
    
    base_info = f"""
    You are a mystical AI tattoo oracle designer, inspired by tarot reading and symbolic divination. 
    Your task is to create a unique, meaningful tattoo design concept based on the following information:
    
    CORE IDENTITY:
    - First Name: {first_name}
    - Last Name: {last_name}
    - Date of Birth: {date_of_birth}
    - Age: {age}
    - Zodiac Sign: {zodiac_sign}
    - Life Path Number: {life_path_number}
    """
    
    # Add optional personalization fields
    additional_info = "\n    DEEPER PERSONALIZATION:"
    
    if birthplace:
        additional_info += f"\n    - Birthplace: {birthplace} (incorporate regional symbolism, geographic elements, or local mythology)"
    
    if favorite_element:
        additional_info += f"\n    - Favorite Element: {favorite_element} (integrate elemental qualities - Fire: bold flames/energy, Water: flowing lines/depth, Earth: grounding/stability, Air: movement/freedom)"
    
    if preferred_aesthetic:
        additional_info += f"\n    - Preferred Aesthetic: {preferred_aesthetic} (design should reflect this visual style and artistic approach)"
    
    if spirit_animal:
        additional_info += f"\n    - Spirit Animal: {spirit_animal} (incorporate this creature's symbolic meaning and characteristics)"
    
    if life_theme:
        additional_info += f"\n    - Life Theme/Value: {life_theme} (weave this concept throughout the design's symbolism)"
    
    if personal_story:
        additional_info += f"\n    - Personal Journey: {personal_story} (honor this experience through symbolic representation)"
    
    if cultural_affiliation:
        additional_info += f"\n    - Cultural/Spiritual Heritage: {cultural_affiliation} (incorporate relevant symbols, patterns, or motifs from this tradition)"
    
    # If no additional info was provided, don't add the section
    if additional_info == "\n    DEEPER PERSONALIZATION:":
        additional_info = ""
    
    format_instructions = """
    
    Please provide your response in the following JSON format:
    {
        "symbolic_analysis": "Interpret name numerology, zodiac sign, and any relevant symbolic meanings derived from all provided information. Weave together the personal elements into a cohesive narrative.",
        "core_tattoo_theme": "Describe the emotional, spiritual, or archetypal essence the tattoo should express, incorporating the deeper personalization elements.",
        "visual_motif_description": "Provide a vivid, imaginative description of the tattoo's visual elements (symbols, shapes, animals, patterns, etc.) that incorporates the specified aesthetic preferences, elements, and cultural influences.",
        "placement_suggestion": "Recommend ideal body placement and size (e.g., upper forearm, chest, sleeve, ankle) considering the design's complexity and personal significance.",
        "mystical_insight": "End with a brief fortune-style message tied to the design meaning and the person's journey.",
        "image_prompt": "A detailed prompt for generating the tattoo image, describing the visual elements in a way suitable for AI image generation. Include specific style, cultural elements, and aesthetic preferences mentioned."
    }
    
    DESIGN GUIDELINES:
    - Create a mythic story that connects all the personal elements provided
    - If birthplace is mentioned, incorporate geographic or regional symbolism
    - If elemental preference is given, let it influence the design's texture and flow
    - If aesthetic preference is specified, ensure the design reflects that artistic style
    - If spirit animal is mentioned, make it central to the design's meaning
    - If life theme is provided, let it guide the overall symbolic message
    - If personal story is shared, honor it through metaphorical representation
    - If cultural affiliation is mentioned, respectfully incorporate authentic elements
    
    Style & Tone:
    - Mysterious yet poetic
    - Tarot card reader meets visionary tattoo artist
    - Use rich metaphors and artistic vocabulary
    - Avoid generic or overused symbols—focus on originality and meaningful storytelling
    - Each reading should be completely unique and deeply personalized
    - Tell a short mythic story of this person's journey and destiny
    
    Make sure the response is valid JSON and each field contains meaningful, unique content based on ALL the person's provided information.
    """
    
    return base_info + additional_info + format_instructions

def generate_tattoo_reading_with_openrouter(first_name, last_name, date_of_birth, age, zodiac_sign, life_path_number,
                                          birthplace=None, favorite_element=None, preferred_aesthetic=None, 
                                          spirit_animal=None, life_theme=None, personal_story=None, cultural_affiliation=None):
    """Generate a unique tattoo reading using OpenRouter as backup"""
    
    prompt = build_enhanced_prompt(first_name, last_name, date_of_birth, age, zodiac_sign, life_path_number,
                                 birthplace, favorite_element, preferred_aesthetic, spirit_animal, 
                                 life_theme, personal_story, cultural_affiliation)
    
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
            "max_tokens": 1200,  # Increased for more detailed responses
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

def generate_tattoo_reading_with_chatgpt(first_name, last_name, date_of_birth, age, zodiac_sign, life_path_number,
                                        birthplace=None, favorite_element=None, preferred_aesthetic=None, 
                                        spirit_animal=None, life_theme=None, personal_story=None, cultural_affiliation=None):
    """Generate a unique tattoo reading using ChatGPT (primary)"""
    
    prompt = build_enhanced_prompt(first_name, last_name, date_of_birth, age, zodiac_sign, life_path_number,
                                 birthplace, favorite_element, preferred_aesthetic, spirit_animal, 
                                 life_theme, personal_story, cultural_affiliation)
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a mystical AI tattoo oracle designer. Always respond with valid JSON format."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1200,  # Increased for more detailed responses
            temperature=0.8
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating ChatGPT response: {e}")
        return None

def generate_tattoo_reading_with_fallback(first_name, last_name, date_of_birth, age, zodiac_sign, life_path_number,
                                        birthplace=None, favorite_element=None, preferred_aesthetic=None, 
                                        spirit_animal=None, life_theme=None, personal_story=None, cultural_affiliation=None):
    """Generate tattoo reading with ChatGPT primary and OpenRouter fallback"""
    
    # Try ChatGPT first
    if openai.api_key:
        chatgpt_response = generate_tattoo_reading_with_chatgpt(
            first_name, last_name, date_of_birth, age, zodiac_sign, life_path_number,
            birthplace, favorite_element, preferred_aesthetic, spirit_animal, 
            life_theme, personal_story, cultural_affiliation
        )
        if chatgpt_response:
            return chatgpt_response, "chatgpt"
    
    # Fallback to OpenRouter
    if OPENROUTER_API_KEY:
        openrouter_response = generate_tattoo_reading_with_openrouter(
            first_name, last_name, date_of_birth, age, zodiac_sign, life_path_number,
            birthplace, favorite_element, preferred_aesthetic, spirit_animal, 
            life_theme, personal_story, cultural_affiliation
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

def generate_placeholder_image(first_name, last_name):
    """Generate a placeholder when all image services fail"""
    # You could create a simple text-based image or use a default image
    # For now, return None to indicate no image available
    return None

def generate_tattoo_image_with_complete_fallback(image_prompt, first_name, last_name):
    """Try multiple image generation services in order"""
    
    # 1. Try DALL-E (OpenAI)
    if openai.api_key:
        image_path = generate_image_with_dalle(image_prompt, first_name, last_name)
        if image_path:
            return image_path, "dalle"
    
    # 2. Try Stability AI
    if STABILITY_API_KEY:
        image_path = generate_image_with_stability(image_prompt, first_name, last_name)
        if image_path:
            return image_path, "stability"
    
    # 3. Fallback to placeholder or no image
    return generate_placeholder_image(first_name, last_name), "placeholder"

@tattoo_bp.route("/generate_tattoo", methods=["POST"])
def generate_tattoo():
    data = request.get_json()
    
    # Core required fields
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    date_of_birth = data.get("date_of_birth")
    age = data.get("age")
    
    # Optional personalization fields
    birthplace = data.get("birthplace")
    favorite_element = data.get("favorite_element")
    preferred_aesthetic = data.get("preferred_aesthetic")
    spirit_animal = data.get("spirit_animal")
    life_theme = data.get("life_theme")
    personal_story = data.get("personal_story")
    cultural_affiliation = data.get("cultural_affiliation")

    # Validation for required fields
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

    # Generate unique reading with enhanced personalization and fallback system
    ai_response, text_provider = generate_tattoo_reading_with_fallback(
        first_name, last_name, date_of_birth, age, zodiac_sign, life_path_number,
        birthplace, favorite_element, preferred_aesthetic, spirit_animal, 
        life_theme, personal_story, cultural_affiliation
    )
    
    if not ai_response:
        return jsonify({"error": "Failed to generate tattoo reading - all AI services unavailable"}), 500
    
    try:
        reading_data = json.loads(ai_response)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid response format from AI"}), 500
    
    # Generate image based on the AI's description with complete fallback
    image_path, image_provider = generate_tattoo_image_with_complete_fallback(
        reading_data.get("image_prompt", ""), first_name, last_name
    )
    
    # Prepare response
    response_data = {
        "symbolic_analysis": reading_data.get("symbolic_analysis", ""),
        "core_tattoo_theme": reading_data.get("core_tattoo_theme", ""),
        "visual_motif_description": reading_data.get("visual_motif_description", ""),
        "placement_suggestion": reading_data.get("placement_suggestion", ""),
        "mystical_insight": reading_data.get("mystical_insight", ""),
        "image_prompt": reading_data.get("image_prompt", ""),
        "image_url": image_path if image_path else None,
        "ai_provider": f"text:{text_provider},image:{image_provider}",  # For debugging/monitoring
        "personalization_used": {
            "birthplace": bool(birthplace),
            "favorite_element": bool(favorite_element),
            "preferred_aesthetic": bool(preferred_aesthetic),
            "spirit_animal": bool(spirit_animal),
            "life_theme": bool(life_theme),
            "personal_story": bool(personal_story),
            "cultural_affiliation": bool(cultural_affiliation)
        }
    }

    return jsonify(response_data)

