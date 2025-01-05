from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest, TelegramRetryAfter

from config.integrations import bot
from services.api.openai import get_text_response_in_incognito_mode

admin_router = Router()


async def message_handler(message):
    response_generator = get_text_response_in_incognito_mode(message.text)
    original_message = await message.reply("Loading...")
    original_message_id = original_message.message_id
    print(original_message.message_id)
    response_text = ""
    generator_counter = 0
    global_generator_counter = 0
    last_generated_text_character_counter = 0
    while True:
        global_generator_counter += 1
        generator_counter += 1
        if global_generator_counter % 100 == 0:
            new_message = await message.answer(response_text[last_generated_text_character_counter:])
            original_message_id = new_message.message_id
        try:
            response_text += next(response_generator)
            if generator_counter >= 30:
                await bot.edit_message_text(chat_id=message.chat.id, message_id=original_message_id,
                                            text=response_text)
                generator_counter = 0
        except TelegramBadRequest:
            response_text += next(response_generator)
            if generator_counter >= 30:
                await bot.edit_message_text(chat_id=message.chat.id, message_id=original_message_id,
                                            text=response_text)
                generator_counter = 0
        except StopIteration:
            break
        finally:
            last_generated_text_character_counter = len(response_text)
    await bot.edit_message_text(chat_id=message.chat.id, message_id=original_message_id,
                                text=response_text, parse_mode=ParseMode.MARKDOWN)


admin_router.message.register(message_handler, F.text)
