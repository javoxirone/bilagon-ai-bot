from database.user import User
from aiogram.enums import ParseMode

from aiogram.types import Message
from services.utils import (
    initialize_user,
    get_lang_keyboard,
    get_user_language_by_telegram_id,
)
from templates.message_templates import (
    get_start_command_message,
    get_language_command_message,
    get_help_command_message,
    get_examples_command_message,
    get_settings_command_message,
    get_premium_requests_num_message,
    get_donate_command_message,
)

async def command_start_handler(message: Message) -> None:
    is_registered_user = await initialize_user(message)
    if is_registered_user:
        db = User()
        user = db.get_user_by_telegram_id(message.from_user.id)
        db.close()
        await message.answer(get_start_command_message(user["language"]))


async def command_help_handler(message: Message) -> None:
    is_registered_user = await initialize_user(message)
    if is_registered_user:
        telegram_id = message.from_user.id
        db = User()
        user = db.get_user_by_telegram_id(telegram_id)
        db.close()
        language = user["language"]
        await message.answer(get_help_command_message(language), parse_mode=ParseMode.HTML)


async def command_settings_handler(message: Message) -> None:
    is_registered_user = await initialize_user(message)
    if is_registered_user:
        telegram_id = message.from_user.id
        db = User()
        user = db.get_user_by_telegram_id(telegram_id)
        db.close()
        tariff = "-"
        requests_num = get_premium_requests_num_message(user['language'])
        expiration_date = "-"
        language = user['language']
        await message.answer(get_settings_command_message(tariff, requests_num, expiration_date, language),
                             parse_mode=ParseMode.HTML)


async def command_language_handler(message: Message) -> None:
    is_registered_user = await initialize_user(message)
    if is_registered_user:
        telegram_id = message.from_user.id
        db = User()
        user = db.get_user_by_telegram_id(telegram_id)
        db.close()
        await message.answer(get_language_command_message(user["language"]), reply_markup=get_lang_keyboard())


async def command_examples_handler(message: Message) -> None:
    is_registered_user = await initialize_user(message)
    if is_registered_user:
        telegram_id = message.from_user.id
        db = User()
        user = db.get_user_by_telegram_id(telegram_id)
        db.close()
        language = user["language"]
        await message.answer(get_examples_command_message(language))


async def command_donate_handler(message: Message) -> None:
    is_registered_user = await initialize_user(message)
    if is_registered_user:
        telegram_id = message.from_user.id
        language = get_user_language_by_telegram_id(telegram_id)
        await message.answer(get_donate_command_message(language), parse_mode=ParseMode.HTML)

