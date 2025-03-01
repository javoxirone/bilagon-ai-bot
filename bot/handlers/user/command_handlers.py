from aiogram.enums import ParseMode
from aiogram.types import Message

from keyboards.inline_keyboards import get_lang_keyboard
from services.database.user_database_services import get_user_by_telegram_id, get_user_language
from templates.message_templates import get_language_command_message, get_start_command_message, \
    get_help_command_message, get_donate_command_message, get_examples_command_message


async def command_start_handler(message: Message) -> None:
    user_language = get_user_language(message.from_user.id)
    await message.answer(get_start_command_message(user_language))


async def command_help_handler(message: Message) -> None:
    user_language = get_user_language(message.from_user.id)
    await message.answer(get_help_command_message(user_language), parse_mode=ParseMode.HTML)


async def command_donate_handler(message: Message) -> None:
    user_language = get_user_language(message.from_user.id)
    await message.answer(
        get_donate_command_message(user_language), parse_mode=ParseMode.HTML
    )

async def command_examples_handler(message: Message) -> None:
    user_language = get_user_language(message.from_user.id)
    await message.answer(get_examples_command_message(user_language))

async def command_contribute_handler(message: Message) -> None:
    ...


async def command_settings_handler(message: Message) -> None:
    ...


async def command_language_handler(message: Message) -> None:
    user = get_user_by_telegram_id(message.from_user.id)
    await message.answer(
        get_language_command_message(user["language"]), reply_markup=get_lang_keyboard()
    )
