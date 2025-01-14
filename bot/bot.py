from typing import NoReturn
from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message
from config.integrations import bot
from config.constants import DIVIDE_MESSAGE_AFTER, MESSAGE_COMPLETION_CURSOR
from services.api.openai import get_text_response_in_incognito_mode

admin_router = Router()


async def handle_incognito_message(message: Message) -> NoReturn:
    response_generator = get_text_response_in_incognito_mode(message.text)
    original_message = await message.reply("Loading...")
    original_message_id = original_message.message_id
    dummy_response_text = ""
    generator_counter = 0

    while True:
        generator_counter += 1
        try:
            dummy_response_text += next(response_generator)
            if len(dummy_response_text) >= DIVIDE_MESSAGE_AFTER:
                await bot.edit_message_text(chat_id=message.chat.id, message_id=original_message_id,
                                            text=dummy_response_text[:DIVIDE_MESSAGE_AFTER])
                dummy_response_text = dummy_response_text[DIVIDE_MESSAGE_AFTER:]

                original_message = await message.answer(MESSAGE_COMPLETION_CURSOR)
                original_message_id = original_message.message_id

            if generator_counter >= 30:
                await bot.edit_message_text(chat_id=message.chat.id, message_id=original_message_id,
                                            text=dummy_response_text + MESSAGE_COMPLETION_CURSOR)
                generator_counter = 0

        except TelegramBadRequest:
            dummy_response_text += next(response_generator)
            if len(dummy_response_text) >= DIVIDE_MESSAGE_AFTER:
                await bot.edit_message_text(chat_id=message.chat.id, message_id=original_message_id,
                                            text=dummy_response_text[:DIVIDE_MESSAGE_AFTER])
                dummy_response_text = dummy_response_text[DIVIDE_MESSAGE_AFTER:]
                original_message = await message.answer(MESSAGE_COMPLETION_CURSOR)
                original_message_id = original_message.message_id

            if generator_counter >= 30:
                await bot.edit_message_text(chat_id=message.chat.id, message_id=original_message_id,
                                            text=dummy_response_text + MESSAGE_COMPLETION_CURSOR)
                generator_counter = 0

        except StopIteration:
            break

    while dummy_response_text:
        await bot.edit_message_text(chat_id=message.chat.id, message_id=original_message_id,
                                    text=dummy_response_text[:DIVIDE_MESSAGE_AFTER], parse_mode="Markdown")
        dummy_response_text = dummy_response_text[DIVIDE_MESSAGE_AFTER:]
        if dummy_response_text:
            original_message = await message.answer(MESSAGE_COMPLETION_CURSOR)
            original_message_id = original_message.message_id

async def message_handler(message: Message) -> NoReturn:


admin_router.message.register(message_handler, F.text)
