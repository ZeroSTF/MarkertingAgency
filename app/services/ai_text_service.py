import requests

class AiTextService:
    API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent'

    def __init__(self, api_key):
        self.api_key = api_key

    def generate_ad_copy(self, prompt):
        enhanced_prompt = f"Create a professional and attractive social media advertisement for the following product or service: {prompt}. The ad should be engaging, highlight key benefits, and include a call to action. Keep it concise and impactful."
        return self._generate_content(enhanced_prompt)

    def _generate_content(self, prompt):
        headers = {'Content-Type': 'application/json'}
        body = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 1024,
                "stopSequences": []
            }
        }
        response = requests.post(f"{self.API_URL}?key={self.api_key}", json=body, headers=headers)
        response.raise_for_status()
        return response.json()['candidates'][0]['content']['parts'][0]['text']