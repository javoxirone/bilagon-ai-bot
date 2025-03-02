import asyncio
from aiogram.exceptions import TelegramBadRequest, TelegramRetryAfter
from config.constants import DIVIDE_MESSAGE_AFTER, MESSAGE_COMPLETION_CURSOR
from config.integrations import bot
from utils.common.format_common_utils import format_response_chunk
from utils.handler.text_handler_utils import send_message_chunk, send_remaining_chunks


async def process_streaming_response(chat_id, original_message_id, response_generator, user_language):
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
                    await send_message_chunk(
                        chat_id,
                        original_message_id,
                        dummy_response_text[:DIVIDE_MESSAGE_AFTER]
                    )
                    dummy_response_text = dummy_response_text[DIVIDE_MESSAGE_AFTER:]
                    original_message = await bot.send_message(chat_id, MESSAGE_COMPLETION_CURSOR)
                    original_message_id = original_message.message_id

                generator_counter += 1
                if generator_counter >= 80:
                    await send_message_chunk(
                        chat_id,
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

    await send_remaining_chunks(chat_id, original_message_id, dummy_response_text, user_language)
    return assistant_response_message
