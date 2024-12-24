import os
from dotenv import load_dotenv
load_dotenv()

# Telegram bot constants
BOT_TOKEN = os.getenv('BOT_TOKEN')

# External API constants
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Webhook constants
WEB_SERVER_HOST = os.getenv('WEB_SERVER_HOST')
WEB_SERVER_PORT = os.getenv('WEB_SERVER_PORT')
WEBHOOK_PATH = os.getenv('WEBHOOK_PATH')
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET')
BASE_WEBHOOK_URL = os.getenv("BASE_WEBHOOK_URL")
