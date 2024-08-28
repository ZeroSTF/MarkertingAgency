from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import requests

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# Configure OpenAI API
API_KEY = os.getenv("GEMINI_API_KEY")

API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent'

@app.route('/')
def home():
    return "Welcome to the AI Marketing Agency API"

@app.route('/generate-copy', methods=['POST'])
def generate_copy():
    data = request.json
    prompt = data.get('prompt', '')
    
    enhanced_prompt = f"Créez une publicité (ready for copy and paste in my post, you can use emojis) professionnelle et attrayante pour les médias sociaux pour le produit ou service suivant : {prompt}. La publicité doit être engageante, mettre en évidence les principaux avantages et inclure un appel à l'action. Gardez-la concise et percutante."
    
    try:
        response = generate_content(enhanced_prompt)
        return jsonify({"ad_copy": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate-title', methods=['POST'])
def generate_title():
    data = request.json
    description = data.get('description', '')
    
    prompt = f"Générez un titre attrayant pour la publicité d'aprés la description suivante: '{description}' (limitez le titre à 30 caracteres maximum)"
    
    try:
        response = generate_content(prompt)
        return jsonify({"title": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate-hashtags', methods=['POST'])
def generate_hashtags():
    data = request.json
    description = data.get('description', '')
    
    prompt = f"Générez 5 hashtags pertinents et tendance pour le produit ou service suivant : {description}"
    
    try:
        response = generate_content(prompt)
        hashtags = [tag for tag in response.split() if tag.startswith('#')]
        return jsonify({"hashtags": hashtags})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def generate_content(prompt):
    headers = {
        'Content-Type': 'application/json',
    }

    body = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 1024,
            "stopSequences": []
        }
    }

    response = requests.post(f"{API_URL}?key={API_KEY}", headers=headers, json=body)
    response.raise_for_status()
    
    content = response.json()
    return content['candidates'][0]['content']['parts'][0]['text']

if __name__ == '__main__':
    app.run(debug=True)