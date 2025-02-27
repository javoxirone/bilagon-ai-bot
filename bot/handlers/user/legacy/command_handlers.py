from aiogram.enums import ParseMode

from aiogram.types import Message
from services.legacy.utils import (
    get_single_user,
    get_language_of_single_user,
)
from keyboards.inline_keyboards import get_lang_keyboard, get_chat_mode_keyboard
from templates.message_templates import (
    get_start_command_message,
    get_language_command_message,
    get_help_command_message,
    get_examples_command_message,
    get_settings_command_message,
    get_premium_requests_num_message,
    get_donate_command_message, get_chat_mode_message,
)


async def command_start_handler(message: Message) -> None:
    user = get_single_user(message.from_user.id)
    await message.answer(get_start_command_message(user["language"]))


async def command_help_handler(message: Message) -> None:
    language = get_language_of_single_user(message.from_user.id)
    await message.answer(get_help_command_message(language), parse_mode=ParseMode.HTML)


async def command_settings_handler(message: Message) -> None:
    telegram_id: int = message.from_user.id
    user: dict = get_single_user(telegram_id)
    tariff = "-"
    requests_num = get_premium_requests_num_message(user["language"])
    expiration_date = "-"
    language = user["language"]
    await message.answer(
        get_settings_command_message(tariff, requests_num, expiration_date, language),
        parse_mode=ParseMode.HTML,
    )

async def command_mode_handler(message: Message) -> None:
    telegram_id: int = message.from_user.id
    user: dict = get_single_user(telegram_id)
    language: str = user["language"]
    await message.answer(
        get_chat_mode_message(language),
        reply_markup=get_chat_mode_keyboard(language),
        parse_mode=ParseMode.HTML,
    )

async def command_language_handler(message: Message) -> None:
    user = get_single_user(message.from_user.id)
    await message.answer(
        get_language_command_message(user["language"]), reply_markup=get_lang_keyboard()
    )


async def command_examples_handler(message: Message) -> None:
    language = get_language_of_single_user(message.from_user.id)
    await message.answer(get_examples_command_message(language))


async def command_donate_handler(message: Message) -> None:
    language = get_language_of_single_user(message.from_user.id)
    await message.answer(
        get_donate_command_message(language), parse_mode=ParseMode.HTML
    )
