from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, ReplyKeyboardRemove

from config.integrations import bot
from keyboards.inline_keyboards import get_settings_keyboard, get_lang_keyboard, build_models_keyboard
from keyboards.keyboards import build_suggested_questions_keyboard
from services.sdk.openai_sdk_services import get_structured_suggested_questions_with_context
from services.database.conversation_database_services import delete_all_user_conversations
from services.database.user_database_services import update_user_language, get_user_language, \
    update_user_saved_conversation_mode, get_user_saved_conversation_mode, get_user_model_name, update_user_model
from templates.message_templates import get_new_chat_message, get_suggestions_message, get_no_suggestions_message, \
    get_activated_context_message, get_settings_command_message, get_language_command_message, get_models_message, \
    get_models


async def process_callback_intro_uz_lang(callback_query: CallbackQuery):
    telegram_id = callback_query.from_user.id
    update_user_language(telegram_id, "uz")
    await bot.delete_message(telegram_id, callback_query.message.message_id)
    await bot.send_message(telegram_id, "O'zbek tili tanlandi, savolingizga javob berishga tayyorman 😊",
                           reply_markup=None)


async def process_callback_intro_ru_lang(callback_query: CallbackQuery):
    telegram_id = callback_query.from_user.id
    update_user_language(telegram_id, "ru")
    await bot.delete_message(telegram_id, callback_query.message.message_id)
    await bot.send_message(telegram_id, "Выбран русский язык, я готов ответить на ваши вопросы 😊", reply_markup=None)


async def process_callback_intro_en_lang(callback_query: CallbackQuery):
    telegram_id = callback_query.from_user.id
    update_user_language(telegram_id, "en")
    await bot.delete_message(telegram_id, callback_query.message.message_id)
    await bot.send_message(telegram_id, "English language selected, I am ready to answer your questions 😊",
                           reply_markup=None)


def get_final_settings_command_message(telegram_id):
    user_language = get_user_language(telegram_id)
    user_saved_conversation_mode = get_user_saved_conversation_mode(telegram_id)
    user_model_name = get_user_model_name(telegram_id)
    return get_settings_command_message(telegram_id, user_language, user_saved_conversation_mode, user_model_name)


async def process_callback_back_to_settings(callback_query: CallbackQuery):
    telegram_id = callback_query.from_user.id
    user_language = get_user_language(telegram_id)
    await bot.edit_message_text(chat_id=telegram_id,
                                message_id=callback_query.message.message_id,
                                text=get_final_settings_command_message(telegram_id),
                                parse_mode=ParseMode.HTML,
                                reply_markup=get_settings_keyboard(user_language))


async def process_callback_uz_lang(callback_query: CallbackQuery):
    telegram_id = callback_query.from_user.id
    update_user_language(telegram_id, "uz")
    user_language = get_user_language(telegram_id)
    await bot.edit_message_text(chat_id=telegram_id,
                                message_id=callback_query.message.message_id,
                                text=get_final_settings_command_message(telegram_id),
                                parse_mode=ParseMode.HTML,
                                reply_markup=get_settings_keyboard(user_language))


async def process_callback_ru_lang(callback_query: CallbackQuery):
    telegram_id = callback_query.from_user.id
    update_user_language(telegram_id, "ru")
    user_language = get_user_language(telegram_id)
    await bot.edit_message_text(chat_id=telegram_id,
                                message_id=callback_query.message.message_id,
                                text=get_final_settings_command_message(telegram_id),
                                parse_mode=ParseMode.HTML,
                                reply_markup=get_settings_keyboard(user_language))


async def process_callback_en_lang(callback_query: CallbackQuery):
    telegram_id = callback_query.from_user.id
    update_user_language(telegram_id, "en")
    user_language = get_user_language(telegram_id)
    await bot.edit_message_text(chat_id=telegram_id,
                                message_id=callback_query.message.message_id,
                                text=get_final_settings_command_message(telegram_id),
                                parse_mode=ParseMode.HTML,
                                reply_markup=get_settings_keyboard(user_language))


async def process_callback_new_chat(callback_query: CallbackQuery):
    telegram_id = callback_query.from_user.id
    user_language = get_user_language(telegram_id)
    delete_all_user_conversations(telegram_id)
    await bot.send_message(telegram_id, get_new_chat_message(user_language), reply_markup=ReplyKeyboardRemove())


async def process_callback_activate_context(callback_query: CallbackQuery):
    telegram_id = callback_query.from_user.id
    user_language = get_user_language(telegram_id)
    update_user_saved_conversation_mode(telegram_id, True)
    await bot.send_message(telegram_id, get_activated_context_message(user_language),
                           reply_markup=ReplyKeyboardRemove())


async def process_toggle_saved_conversation_mode(callback_query: CallbackQuery):
    telegram_id = callback_query.from_user.id
    user_language = get_user_language(telegram_id)
    user_saved_conversation_mode = get_user_saved_conversation_mode(telegram_id)
    update_user_saved_conversation_mode(telegram_id, not user_saved_conversation_mode)
    await bot.edit_message_text(chat_id=telegram_id,
                                message_id=callback_query.message.message_id,
                                text=get_final_settings_command_message(telegram_id),
                                parse_mode=ParseMode.HTML,
                                reply_markup=get_settings_keyboard(user_language))


async def process_switch_language(callback_query: CallbackQuery):
    telegram_id = callback_query.from_user.id
    user_language = get_user_language(telegram_id)
    await bot.edit_message_text(
        chat_id=telegram_id,
        message_id=callback_query.message.message_id,
        text=get_language_command_message(user_language),
        reply_markup=get_lang_keyboard(user_language)
    )


async def process_switch_model(callback_query: CallbackQuery):
    telegram_id = callback_query.from_user.id
    user_language = get_user_language(telegram_id)
    user_model = get_user_model_name(telegram_id)
    await bot.edit_message_text(
        chat_id=telegram_id,
        message_id=callback_query.message.message_id,
        text=get_models_message(user_language),
        reply_markup=build_models_keyboard(get_models(user_language), user_model, user_language)
    )


async def process_model_selection(callback_query: CallbackQuery):
    telegram_id = callback_query.from_user.id
    user_language = get_user_language(telegram_id)
    update_user_model(telegram_id, callback_query.data)
    await bot.edit_message_text(chat_id=telegram_id,
                                message_id=callback_query.message.message_id,
                                text=get_final_settings_command_message(telegram_id),
                                parse_mode=ParseMode.HTML,
                                reply_markup=get_settings_keyboard(user_language))


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
            reply_markup=ReplyKeyboardRemove()
        )
