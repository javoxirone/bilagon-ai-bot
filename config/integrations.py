from aiogram import Bot
from aiogram.enums import ParseMode

from api.openai.processors.text import TextProcessor
from config.constants import OPENAI_API_KEY, OPENAI_BASE_URL, BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
text_processor = TextProcessor(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
