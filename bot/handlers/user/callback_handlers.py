from aiogram.types import CallbackQuery

from config.integrations import bot
from keyboards.keyboards import build_suggested_questions_keyboard
from services.api.openai_api_services import get_structured_suggested_questions_with_context
from services.database.conversation_database_services import delete_all_user_conversations
from services.database.user_database_services import update_user_language, get_user_by_telegram_id, get_user_language
from templates.message_templates import get_new_chat_message, get_suggestions_message, get_no_suggestions_message


async def process_callback_uz_lang(callback_query: CallbackQuery):
    telegram_id = callback_query.from_user.id
    update_user_language(telegram_id, "uz")
    await bot.delete_message(telegram_id, callback_query.message.message_id)
    await bot.send_message(telegram_id, "O'zbek tili tanlandi, savolingizga javob berishga tayyorman 😊",
                           reply_markup=None)


async def process_callback_ru_lang(callback_query: CallbackQuery):
    telegram_id = callback_query.from_user.id
    update_user_language(telegram_id, "ru")
    await bot.delete_message(telegram_id, callback_query.message.message_id)
    await bot.send_message(telegram_id, "Выбран русский язык, я готов ответить на ваши вопросы 😊", reply_markup=None)


async def process_callback_en_lang(callback_query: CallbackQuery):
    telegram_id = callback_query.from_user.id
    update_user_language(telegram_id, "en")
    await bot.delete_message(telegram_id, callback_query.message.message_id)
    await bot.send_message(telegram_id, "English language selected, I am ready to answer your questions 😊",
                           reply_markup=None)


async def process_callback_new_chat(callback_query: CallbackQuery):
    telegram_id = callback_query.from_user.id
    user_language = get_user_language(telegram_id)
    delete_all_user_conversations(telegram_id)
    await bot.send_message(telegram_id, get_new_chat_message(user_language), reply_markup=None)


async def process_callback_suggestions(callback_query: CallbackQuery):
    telegram_id = callback_query.from_user.id
    user_language = get_user_language(telegram_id)
    options = get_structured_suggested_questions_with_context(telegram_id)
    if len(options) > 0:
        await bot.send_message(
            telegram_id,
            get_suggestions_message(user_language),
            reply_markup=build_suggested_questions_keyboard(options)
        )
    else:
        await bot.send_message(
            telegram_id,
            get_no_suggestions_message(user_language),
            reply_markup=None
        )
