from aiogram.enums import ParseMode
from aiogram.types import Message

from keyboards.inline_keyboards import get_settings_keyboard
from services.database.user_database_services import get_user_language, \
    get_user_saved_conversation_mode, get_user_model_name
from templates.message_templates import get_start_command_message, \
    get_help_command_message, get_donate_command_message, get_examples_command_message, get_contribute_message, \
    get_settings_command_message


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
    user_language = get_user_language(message.from_user.id)
    await message.answer(get_contribute_message(user_language), parse_mode=ParseMode.MARKDOWN)


async def command_settings_handler(message: Message) -> None:
    telegram_id = message.from_user.id
    user_language = get_user_language(message.from_user.id)
    saved_conversation_mode = get_user_saved_conversation_mode(message.from_user.id)
    user_model_name = get_user_model_name(telegram_id)
    await message.answer(
        get_settings_command_message(telegram_id, user_language, saved_conversation_mode, user_model_name),
        parse_mode=ParseMode.HTML, reply_markup=get_settings_keyboard(user_language))
