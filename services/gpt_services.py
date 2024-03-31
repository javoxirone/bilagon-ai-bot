from openai import OpenAIError
from templates.message_templates import (
    get_loading_message,
    get_openai_error_message,
    get_bot_error_message,
)
from keyboards.inline_keyboards import get_new_chat_keyboard
from config.integrations import gpt
from aiogram.exceptions import TelegramBadRequest
from services.conversation_services import (
    add_message_of_user_to_conversation,
    add_message_of_assistant_to_conversation,
    get_conversations_of_single_user,
)
from typing import TypedDict
from aiogram import Bot
from aiogram.enums import ParseMode
from config.constants import TOKEN
from services.utils import get_language_of_single_user


bot = Bot(token=TOKEN, parse_mode=ParseMode.MARKDOWN)


class Request(TypedDict):
    telegram_id: int
    text: str
    bot_message_id: int
    language: str


# TODO: need to be refactored, and maybe allocated to another file and folder
async def handle_gpt_response(telegram_id: int, message: list) -> None:
    request_message_id, request_message = message
    text = ""
    language = get_language_of_single_user(telegram_id)
    bot_message = await bot.send_message(
        telegram_id,
        get_loading_message(language),
        reply_to_message_id=request_message_id,
    )
    bot_message_id = bot_message.message_id

    try:
        add_message_of_user_to_conversation(telegram_id, request_message)
        messages = get_conversations_of_single_user(telegram_id)

        stream = gpt.generate_response(max_tokens=2000, messages=messages)
        chunks = []
        counter = 0
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                chunks.append(chunk.choices[0].delta.content)
                counter += 1
                if counter >= 30:
                    await bot.edit_message_text(
                        "".join(chunks) + " ▌",
                        telegram_id,
                        bot_message_id,
                        parse_mode=None,
                        reply_markup=get_new_chat_keyboard(language),
                    )
                    counter = 0

        text = "".join(chunks)
        await bot.edit_message_text(
            text,
            telegram_id,
            bot_message_id,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_new_chat_keyboard(language),
        )
        add_message_of_assistant_to_conversation(telegram_id, text)

    except OpenAIError as e:
        print(e)
        await bot.edit_message_text(
            get_openai_error_message(language),
            telegram_id,
            bot_message_id,
            parse_mode=ParseMode.HTML,
            reply_markup=get_new_chat_keyboard(language),
        )
    except TelegramBadRequest as e:
        print(e)

    except Exception as e:
        print(e)
        if text:
            await bot.edit_message_text(
                text,
                telegram_id,
                bot_message_id,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_new_chat_keyboard(language),
            )
            return
        await bot.edit_message_text(
            get_bot_error_message(language),
            telegram_id,
            bot_message_id,
            parse_mode=ParseMode.HTML,
            reply_markup=get_new_chat_keyboard(language),
        )
