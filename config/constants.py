import os
from dotenv import load_dotenv

load_dotenv()

# Telegram bot constants
BOT_TOKEN: str = os.getenv('BOT_TOKEN')
DIVIDE_MESSAGE_AFTER: int = 4096
MESSAGE_COMPLETION_CURSOR: str = " ▌"

# External API constants
OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY')
OPENAI_BASE_URL: str = os.getenv('OPENAI_BASE_URL')
MODELS = {
    'gpt-4o-mini': 'Fast, smart, general use',
    'gpt-3.5-turbo': 'Balanced, chat, coding, writing',
    'gemini-2.0-flash': 'Ultra-fast, real-time responses',
    'gemini-1.5-flash': 'Fast, automation, quick replies',
    'gemini-1.5-pro': 'Smarter, reasoning, complex tasks',
    'deepseek-chat': 'Coming soon',
    'deepseek-reasoner': 'Coming soon',
    '1o-mini': 'Coming soon',
    '3o-mini': 'Coming soon',
    '3o': 'Coming soon',
    '1o': 'Coming soon',
    'gpt-4o': 'Coming soon',
    'grok-2-1212': 'Coming soon',
}
# 'deepseek-chat': 'General AI, conversations, queries',
# 'deepseek-reasoner': 'Strong logic, problem-solving',
# '1o-mini': 'Lightweight, simple, fast tasks',
# '3o-mini': 'Small, general-purpose AI',
# '3o': 'Balanced, coding, reasoning',
# '1o': 'Compact, basic problem-solving',
# 'gpt-4o': 'Advanced, multimodal, high intelligence',
# 'grok-2-1212': 'Research, reasoning, technical use',
MODEL_LIST: tuple = (
    'gpt-4o-mini',
    'gpt-3.5-turbo',
    'gemini-2.0-flash',
    'gemini-1.5-flash',
    'gemini-1.5-pro',
    '1o-mini',
    '3o-mini',
    '3o',
    '1o',
    'gpt-4o',
    'grok-2-1212',
)

# Webhook constants
WEB_SERVER_HOST: str = os.getenv('WEB_SERVER_HOST')
WEB_SERVER_PORT: str = os.getenv('WEB_SERVER_PORT')
WEBHOOK_PATH: str = os.getenv('WEBHOOK_PATH')
WEBHOOK_SECRET: str = os.getenv('WEBHOOK_SECRET')
BASE_WEBHOOK_URL: str = os.getenv("BASE_WEBHOOK_URL")

# DataBase constants

DB_NAME: str = os.getenv('DB_NAME')
DB_HOST: str = os.getenv('DB_HOST')
DB_USER: str = os.getenv('DB_USER')
DB_PORT: str = os.getenv('DB_PORT')
DB_PASSWORD: str = os.getenv('DB_PASSWORD')
