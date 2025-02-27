from aiogram.types import Message

from keyboards.inline_keyboards import get_lang_keyboard
from services.database.user import get_user_by_telegram_id
from templates.message_templates import get_language_command_message


async def command_start_handler(message: Message) -> None:
    ...

async def command_help_handler(message: Message) -> None:
    ...

async def command_donate_handler(message: Message) -> None:
    ...

async def command_contribute_handler(message: Message) -> None:
    ...

async def command_settings_handler(message: Message) -> None:
    ...

async def command_language_handler(message: Message) -> None:
    user = get_user_by_telegram_id(message.from_user.id)
    await message.answer(
        get_language_command_message(user["language"]), reply_markup=get_lang_keyboard()
    )
