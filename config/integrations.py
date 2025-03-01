from aiogram import Bot

from api.openai.processors.audio import AudioProcessor
from api.openai.processors.text import TextProcessor
from config.constants import OPENAI_API_KEY, OPENAI_BASE_URL, BOT_TOKEN
from decorator.status_message_manager import StatusMessageManager
from parser.document import DocumentParser

bot = Bot(token=BOT_TOKEN)
text_processor = TextProcessor(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
audio_processor = AudioProcessor(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
document_parser = DocumentParser()
status_manager = StatusMessageManager(bot)