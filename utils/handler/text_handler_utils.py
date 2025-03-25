from aiogram.enums import ParseMode
from config.constants import DIVIDE_MESSAGE_AFTER, MESSAGE_COMPLETION_CURSOR
from config.integrations import bot
from keyboards.inline_keyboards import get_message_keyboard, get_incognito_message_keyboard
from services.database.user_database_services import get_user_saved_conversation_mode


async def send_message_chunk(chat_id, message_id, text, reply_markup=None):
    """Send a chunk of text as a Telegram message."""
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )


async def send_remaining_chunks(chat_id, original_message_id, text, user_language):
    """Send any remaining text chunks and add keyboard to the last one."""
    user_saved_conversation_mode = get_user_saved_conversation_mode(chat_id)
    while text:
        if user_saved_conversation_mode:
            reply_markup = get_message_keyboard(user_language) if len(text) <= DIVIDE_MESSAGE_AFTER else None
        else:
            reply_markup = get_incognito_message_keyboard(user_language) if len(text) <= DIVIDE_MESSAGE_AFTER else None

        await send_message_chunk(
            chat_id,
            original_message_id,
            text[:DIVIDE_MESSAGE_AFTER],
            reply_markup
        )
        text = text[DIVIDE_MESSAGE_AFTER:]

        if text:
            original_message = await bot.send_message(chat_id, MESSAGE_COMPLETION_CURSOR)
            original_message_id = original_message.message_id
