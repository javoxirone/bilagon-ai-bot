from aiogram.enums import ParseMode
from config.constants import DIVIDE_MESSAGE_AFTER, MESSAGE_COMPLETION_CURSOR
from config.integrations import bot
from keyboards.inline_keyboards import get_new_chat_keyboard



async def send_message_chunk(chat_id, message_id, text, reply_markup=None):
    """Send a chunk of text as a Telegram message."""
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )


async def send_remaining_chunks(message, original_message_id, text, user_language):
    """Send any remaining text chunks and add keyboard to the last one."""
    while text:
        reply_markup = get_new_chat_keyboard(user_language) if len(text) <= DIVIDE_MESSAGE_AFTER else None

        await send_message_chunk(
            message.chat.id,
            original_message_id,
            text[:DIVIDE_MESSAGE_AFTER],
            reply_markup
        )
        text = text[DIVIDE_MESSAGE_AFTER:]

        if text:
            original_message = await message.answer(MESSAGE_COMPLETION_CURSOR)
            original_message_id = original_message.message_id
