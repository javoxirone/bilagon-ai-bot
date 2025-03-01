from aiogram.types import CallbackQuery

from config.integrations import bot
from services.database.conversation_database_services import delete_all_user_conversations
from services.database.user_database_services import update_user_language, get_user_by_telegram_id
from templates.message_templates import get_new_chat_message


async def process_callback_uz_lang(callback_query: CallbackQuery):
    telegram_id = callback_query.from_user.id
    update_user_language(telegram_id, "uz")
    await bot.delete_message(telegram_id, callback_query.message.message_id)
    await bot.send_message(telegram_id, "O'zbek tili tanlandi, savolingizga javob berishga tayyorman 😊")


async def process_callback_ru_lang(callback_query: CallbackQuery):
    telegram_id = callback_query.from_user.id
    update_user_language(telegram_id, "ru")
    await bot.delete_message(telegram_id, callback_query.message.message_id)
    await bot.send_message(telegram_id, "Выбран русский язык, я готов ответить на ваши вопросы 😊")


async def process_callback_en_lang(callback_query: CallbackQuery):
    telegram_id = callback_query.from_user.id
    update_user_language(telegram_id, "en")
    await bot.delete_message(telegram_id, callback_query.message.message_id)
    await bot.send_message(telegram_id, "English language selected, I am ready to answer your questions 😊")


async def process_callback_new_chat(callback_query: CallbackQuery):
    telegram_id = callback_query.from_user.id
    user = get_user_by_telegram_id(telegram_id)
    delete_all_user_conversations(telegram_id)
    await bot.send_message(telegram_id, get_new_chat_message(user["language"]))
