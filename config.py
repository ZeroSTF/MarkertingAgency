import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    DALLE_API_KEY = os.getenv('DALLE_API_KEY')
    FACEBOOK_ACCESS_TOKEN = os.getenv('FACEBOOK_ACCESS_TOKEN')
    FACEBOOK_AD_ACCOUNT_ID = os.getenv('FACEBOOK_AD_ACCOUNT_ID')