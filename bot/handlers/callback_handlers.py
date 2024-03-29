
from services.utils import initialize_user
from database.user import User
from config.integrations import bot, gpt
from aiogram.types import CallbackQuery
from templates.message_templates import (get_new_chat_message, )

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


async def process_callback_new_chat(callback_query: CallbackQuery):
    is_registered_user = await initialize_user(callback_query)
    if is_registered_user:
        telegram_id = callback_query.from_user.id
        db = User()
        user = db.get_user_by_telegram_id(telegram_id)
        db.close()
        gpt.reset_chat(telegram_id)
        await bot.send_message(telegram_id, get_new_chat_message(user["language"]))
