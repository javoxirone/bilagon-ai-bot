
from database.user import User
from aiogram.types import CallbackQuery
from templates.message_templates import (get_new_chat_message, )
from config.integrations import gpt
from aiogram import Bot
from config.constants import TOKEN
from aiogram.enums import ParseMode
from decorators.auth_decorators import initialize_user

bot = Bot(token=TOKEN, parse_mode=ParseMode.MARKDOWN)

async def process_callback_uz_lang(callback_query: CallbackQuery):
    telegram_id = callback_query.from_user.id
    db = User()
    db.change_language(telegram_id, callback_query.data)
    db.close()

    await bot.delete_message(telegram_id, callback_query.message.message_id)
    await bot.send_message(telegram_id, "O'zbek tili tanlandi, savolingizga javob berishga tayyorman 😊")


async def process_callback_ru_lang(callback_query: CallbackQuery):
    telegram_id = callback_query.from_user.id
    db = User()
    db.change_language(telegram_id, callback_query.data)
    db.close()

    await bot.delete_message(telegram_id, callback_query.message.message_id)
    await bot.send_message(telegram_id, "Выбран русский язык, я готов ответить на ваши вопросы 😊")


async def process_callback_en_lang(callback_query: CallbackQuery):
    telegram_id = callback_query.from_user.id
    db = User()
    db.change_language(telegram_id, callback_query.data)
    db.close()

    await bot.delete_message(telegram_id, callback_query.message.message_id)
    await bot.send_message(telegram_id, "English language selected, I am ready to answer your questions 😊")

@initialize_user
async def process_callback_new_chat(callback_query: CallbackQuery):
    telegram_id = callback_query.from_user.id
    db = User()
    user = db.get_user_by_telegram_id(telegram_id)
    db.close()
    gpt.reset_chat(telegram_id)
    await bot.send_message(telegram_id, get_new_chat_message(user["language"]))
