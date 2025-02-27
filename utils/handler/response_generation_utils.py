import asyncio
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest, TelegramRetryAfter
from config.constants import DIVIDE_MESSAGE_AFTER, MESSAGE_COMPLETION_CURSOR
from config.integrations import bot
from keyboards.inline_keyboards import get_new_chat_keyboard
from utils.common.format import format_response_chunk


async def process_streaming_response(message, original_message_id, response_generator, user_language):
    """Process streaming response from generator and handle message chunking."""
    dummy_response_text = ""
    assistant_response_message = ""
    generator_counter = 0

    try:
        while True:
            try:
                next_chunk = next(response_generator)

                dummy_response_text += format_response_chunk(next_chunk)
                assistant_response_message += next_chunk

                if len(dummy_response_text) >= DIVIDE_MESSAGE_AFTER:
                    await _send_message_chunk(
                        message.chat.id,
                        original_message_id,
                        dummy_response_text[:DIVIDE_MESSAGE_AFTER]
                    )
                    dummy_response_text = dummy_response_text[DIVIDE_MESSAGE_AFTER:]
                    original_message = await message.answer(MESSAGE_COMPLETION_CURSOR)
                    original_message_id = original_message.message_id

                generator_counter += 1
                if generator_counter >= 80:
                    await _send_message_chunk(
                        message.chat.id,
                        original_message_id,
                        dummy_response_text + MESSAGE_COMPLETION_CURSOR
                    )
                    generator_counter = 0

            except TelegramBadRequest as e:
                continue
            except TelegramRetryAfter as e:
                await asyncio.sleep(e.retry_after)

    except StopIteration:
        pass

    await _send_remaining_chunks(message, original_message_id, dummy_response_text, user_language)
    return assistant_response_message


async def _send_message_chunk(chat_id, message_id, text, reply_markup=None):
    """Send a chunk of text as a Telegram message."""
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )


async def _send_remaining_chunks(message, original_message_id, text, user_language):
    """Send any remaining text chunks and add keyboard to the last one."""
    while text:
        reply_markup = get_new_chat_keyboard(user_language) if len(text) <= DIVIDE_MESSAGE_AFTER else None

        await _send_message_chunk(
            message.chat.id,
            original_message_id,
            text[:DIVIDE_MESSAGE_AFTER],
            reply_markup
        )
        text = text[DIVIDE_MESSAGE_AFTER:]

        if text:
            original_message = await message.answer(MESSAGE_COMPLETION_CURSOR)
            original_message_id = original_message.message_id
