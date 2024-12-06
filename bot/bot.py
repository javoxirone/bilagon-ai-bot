from aiogram.filters import Command
from aiogram import F, Router
from bot.handlers.user.command_handlers import (
    command_start_handler,
    command_help_handler,
    command_examples_handler,
    command_donate_handler,
    command_language_handler,
    command_settings_handler, command_mode_handler,
)
from bot.handlers.user.callback_handlers import (
    process_callback_en_lang,
    process_callback_ru_lang,
    process_callback_uz_lang,
    process_callback_new_chat,
)
from bot.handlers.user.message_handlers import (
    message_handler,
)
from bot.handlers.user.voice_handlers import (
    voice_message_handler,
)
from bot.handlers.user.image_handlers import image_handler
from bot.handlers.user.file_handlers import document_handler

# =========================== BOT CONFIGURATION ===========================

user_router = Router()
admin_router = Router()

# ========================================================================




# =========================== USER ROUTER HANDLERS ===========================

# Command handlers
user_router.message.register(command_start_handler, Command("start"))
user_router.message.register(command_help_handler, Command("help"))
user_router.message.register(command_settings_handler, Command("settings"))
user_router.message.register(command_mode_handler, Command("mode"))
user_router.message.register(command_language_handler, Command("language"))
user_router.message.register(command_examples_handler, Command("examples"))
user_router.message.register(command_donate_handler, Command("donate"))

# Callback handlers
user_router.callback_query.register(process_callback_uz_lang, lambda c: c.data == "uz")
user_router.callback_query.register(process_callback_ru_lang, lambda c: c.data == "ru")
user_router.callback_query.register(process_callback_en_lang, lambda c: c.data == "en")
user_router.callback_query.register(process_callback_new_chat, lambda c: c.data == "new_chat")

# Message handlers
user_router.message.register(message_handler, F.text)

# Media handlers
user_router.message.register(image_handler, F.photo)

# Voice handlers
user_router.message.register(voice_message_handler, F.voice)

# Document handlers
user_router.message.register(document_handler, F.document)

# ===========================================================================



# =========================== ADMIN ROUTER HANDLERS ===========================



# =============================================================================