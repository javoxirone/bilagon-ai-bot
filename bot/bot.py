
from aiogram.filters import Command
from aiogram import F
from bot.handlers.command_handlers import (
    command_start_handler,
    command_help_handler,
    command_examples_handler,
    command_donate_handler,
    command_language_handler,
    command_settings_handler,
)
from bot.handlers.callback_handlers import (
    process_callback_en_lang,
    process_callback_ru_lang,
    process_callback_uz_lang,
    process_callback_new_chat,
)
from bot.handlers.message_handlers import (
    message_handler,
)
from bot.handlers.image_handlers import image_handler
from aiogram import Bot, Dispatcher
from config.constants import TOKEN
from aiogram.enums import ParseMode

bot = Bot(token=TOKEN, parse_mode=ParseMode.MARKDOWN)
dp = Dispatcher()

# Command handlers
dp.message.register(command_start_handler, Command('start'))
dp.message.register(command_help_handler, Command('help'))
dp.message.register(command_settings_handler, Command('settings'))
dp.message.register(command_language_handler, Command('language'))
dp.message.register(command_examples_handler, Command('examples'))
dp.message.register(command_donate_handler, Command('donate'))

# Callback handlers
dp.callback_query.register(process_callback_uz_lang, lambda c: c.data == 'uz')
dp.callback_query.register(process_callback_ru_lang, lambda c: c.data == 'ru')
dp.callback_query.register(process_callback_en_lang, lambda c: c.data == 'en')
dp.callback_query.register(process_callback_new_chat, lambda c: c.data == 'new_chat')

# Message handlers
dp.message.register(message_handler, F.text)

# Media handlers
dp.message.register(image_handler, F.photo)

