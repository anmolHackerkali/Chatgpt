import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_KEY = os.getenv("GROK_API_KEY")
BASE_URL = "https://api.x.ai/v1"
MODEL = "grok-4"
