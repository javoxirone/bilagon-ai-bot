import os
from dotenv import load_dotenv

load_dotenv()

# Telegram bot constants
BOT_TOKEN: str = os.getenv('BOT_TOKEN')
DIVIDE_MESSAGE_AFTER: int = 4096

# External API constants
OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY')
OPENAI_BASE_URL: str = os.getenv('OPENAI_BASE_URL')

# Webhook constants
WEB_SERVER_HOST: str = os.getenv('WEB_SERVER_HOST')
WEB_SERVER_PORT: str = os.getenv('WEB_SERVER_PORT')
WEBHOOK_PATH: str = os.getenv('WEBHOOK_PATH')
WEBHOOK_SECRET: str = os.getenv('WEBHOOK_SECRET')
BASE_WEBHOOK_URL: str = os.getenv("BASE_WEBHOOK_URL")
