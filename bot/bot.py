from aiogram import Router, F
from aiogram.filters import Command

from bot.handlers.user.callback_handlers import process_callback_new_chat, process_callback_uz_lang, \
    process_callback_ru_lang, process_callback_en_lang, process_callback_suggestions, process_callback_activate_context, \
    process_toggle_saved_conversation_mode, process_switch_language, process_switch_model, process_model_selection
from bot.handlers.user.command_handlers import command_start_handler, command_help_handler, \
    command_donate_handler, command_examples_handler, command_contribute_handler, command_settings_handler
from bot.handlers.user.document_handler import handle_document
from bot.handlers.user.photo_handlers import handle_photo
from bot.handlers.user.text_handlers import handle_message
from bot.handlers.user.voice_handlers import handle_voice_message

admin_router = Router()
user_router = Router()

user_router.message.register(command_start_handler, Command("start"))
user_router.message.register(command_help_handler, Command("help"))
user_router.message.register(command_settings_handler, Command("settings"))
user_router.message.register(command_donate_handler, Command("donate"))
user_router.message.register(command_examples_handler, Command("examples"))
user_router.message.register(command_contribute_handler, Command("contribute"))

user_router.callback_query.register(process_callback_uz_lang, lambda c: c.data == "lang_uz")
user_router.callback_query.register(process_callback_ru_lang, lambda c: c.data == "lang_ru")
user_router.callback_query.register(process_callback_en_lang, lambda c: c.data == "lang_en")
user_router.callback_query.register(process_callback_new_chat, lambda c: c.data == "new_chat")
user_router.callback_query.register(process_callback_suggestions, lambda c: c.data == "suggestions")
user_router.callback_query.register(process_callback_activate_context, lambda c: c.data == "activate_context")
user_router.callback_query.register(process_switch_language, lambda c: c.data == "switch_language")
user_router.callback_query.register(process_switch_model, lambda c: c.data == "switch_model")
user_router.callback_query.register(process_model_selection, lambda c: c.data == "gpt-4o-mini")
user_router.callback_query.register(process_model_selection, lambda c: c.data == "gpt-3.5-turbo")
user_router.callback_query.register(process_toggle_saved_conversation_mode,
                                    lambda c: c.data == "toggle_saved_conversation_mode")

user_router.message.register(handle_message, F.text)
user_router.message.register(handle_photo, F.photo)
user_router.message.register(handle_voice_message, F.voice)
user_router.message.register(handle_document, F.document)
user_router.callback_query.register(process_callback_new_chat, F.callbackQuery)
