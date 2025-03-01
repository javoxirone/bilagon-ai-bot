from aiogram import Router, F
from aiogram.filters import Command

from bot.handlers.user.callback_handlers import process_callback_new_chat, process_callback_uz_lang, \
    process_callback_ru_lang, process_callback_en_lang
from bot.handlers.user.command_handlers import command_language_handler
from bot.handlers.user.document_handler import handle_document
from bot.handlers.user.photo_handlers import handle_photo
from bot.handlers.user.text_handlers import handle_message_with_context
from bot.handlers.user.voice_handlers import handle_voice_message

admin_router = Router()
user_router = Router()

user_router.message.register(command_language_handler, Command("language"))

user_router.callback_query.register(process_callback_uz_lang, lambda c: c.data == "lang_uz")
user_router.callback_query.register(process_callback_ru_lang, lambda c: c.data == "lang_ru")
user_router.callback_query.register(process_callback_en_lang, lambda c: c.data == "lang_en")
user_router.callback_query.register(process_callback_new_chat, lambda c: c.data == "new_chat")

user_router.message.register(handle_message_with_context, F.text)
user_router.message.register(handle_photo, F.photo)
user_router.message.register(handle_voice_message, F.voice)
user_router.message.register(handle_document, F.document)
user_router.callback_query.register(process_callback_new_chat, F.callbackQuery)
