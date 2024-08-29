import requests
from PIL import Image
from io import BytesIO

class ImageGenerationService:
    API_URL = "https://api.openai.com/v1/images/generations"

    def __init__(self, api_key):
        self.api_key = api_key

    def generate_image(self, prompt):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "prompt": prompt,
            "n": 1,
            "size": "1024x1024"
        }
        response = requests.post(self.API_URL, headers=headers, json=data)
        response.raise_for_status()
        image_url = response.json()['data'][0]['url']
        return self._download_image(image_url)

    def _download_image(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))