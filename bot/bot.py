from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from config.integrations import bot
from config.constants import DIVIDE_MESSAGE_AFTER
from services.api.openai import get_text_response_in_incognito_mode

admin_router = Router()


async def message_handler(message):
    response_generator = get_text_response_in_incognito_mode(message.text)
    original_message = await message.reply("Loading...")
    original_message_id = original_message.message_id
    print(original_message_id)
    full_response_text = ""
    dummy_response_text = ""
    generator_counter = 0

    while True:
        generator_counter += 1

        try:
            dummy_response_text += next(response_generator)
            if len(dummy_response_text) >= DIVIDE_MESSAGE_AFTER:  # Check if the dummy_response_text exceeds 1000 characters
                await bot.edit_message_text(chat_id=message.chat.id, message_id=original_message_id,
                                            text=dummy_response_text[:DIVIDE_MESSAGE_AFTER])  # Edit the first chunk
                dummy_response_text = dummy_response_text[DIVIDE_MESSAGE_AFTER:]  # Remove the sent chunk

                original_message = await message.answer(" ▌")  # Send a new message
                original_message_id = original_message.message_id  # Update the message ID

            if generator_counter >= 30:
                await bot.edit_message_text(chat_id=message.chat.id, message_id=original_message_id,
                                            text=dummy_response_text)
                generator_counter = 0

        except TelegramBadRequest:
            dummy_response_text += next(response_generator)
            if len(dummy_response_text) >= DIVIDE_MESSAGE_AFTER:
                await bot.edit_message_text(chat_id=message.chat.id, message_id=original_message_id,
                                            text=dummy_response_text[:DIVIDE_MESSAGE_AFTER])
                dummy_response_text = dummy_response_text[DIVIDE_MESSAGE_AFTER:]
                original_message = await message.answer(" ▌")
                original_message_id = original_message.message_id

            if generator_counter >= 30:
                await bot.edit_message_text(chat_id=message.chat.id, message_id=original_message_id,
                                            text=dummy_response_text)
                generator_counter = 0

        except StopIteration:
            break

    # Send the remaining dummy_response_text
    while dummy_response_text:
        await bot.edit_message_text(chat_id=message.chat.id, message_id=original_message_id,
                                    text=dummy_response_text[:DIVIDE_MESSAGE_AFTER], parse_mode=ParseMode.MARKDOWN)
        dummy_response_text = dummy_response_text[DIVIDE_MESSAGE_AFTER:]
        if dummy_response_text:
            original_message = await message.answer(" ▌")
            original_message_id = original_message.message_id


admin_router.message.register(message_handler, F.text)
