from gpt.gpt import OpenAIAPI
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from config.constants import TOKEN

gpt = OpenAIAPI()
bot = Bot(token=TOKEN, parse_mode=ParseMode.MARKDOWN)
dp = Dispatcher()