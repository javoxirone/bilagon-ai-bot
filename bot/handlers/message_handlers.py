from openai import error
from aiogram.types import Message
from database.conversation import Conversation
from templates.message_templates import (
    get_loading_message,
    get_openai_error_message,
    get_bot_error_message,
)
from aiogram.enums import ParseMode
from keyboards.inline_keyboards import get_new_chat_keyboard
from decorators.auth_decorators import initialize_user
from config.integrations import gpt
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from config.constants import TOKEN
from aiogram.enums import ParseMode
from services.utils import get_language_of_single_user
from typing import TypedDict


class Request(TypedDict):
    telegram_id: int
    text: str
    bot_message_id: int
    language: str


bot = Bot(token=TOKEN, parse_mode=ParseMode.MARKDOWN)


# TODO: need to be refactored, and maybe allocated to another file and folder
async def generate_gpt_response(request: Request) -> None:
    text = ""
    telegram_id = request["telegram_id"]
    text = request["text"]
    bot_message_id = request["bot_message_id"]
    language = request["language"]
    try:
        conversation_db = Conversation()
        conversation_db.add_conversation(telegram_id, "user", text)
        messages = conversation_db.get_conversations_by_telegram_id(telegram_id)
        print(messages)
        conversation_db.close()

        result = gpt.generate_response(max_tokens=2000, messages=messages)
        chunks = []
        counter = 0
        for chunk in result:
            chunks.append(chunk.choices[0].delta.get("content", ""))
            counter += 1
            if counter >= 30:
                await bot.edit_message_text(
                    "".join(chunks) + " ▌",
                    telegram_id,
                    bot_message_id,
                    parse_mode=None,
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
        conversation_db = Conversation()
        conversation_db.add_conversation(telegram_id, "assistant", text)
        conversation_db.close()

    except error.OpenAIError as e:
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


# TODO: break down into utility functions
@initialize_user
async def message_handler(message: Message) -> None:
    """
    Gets the user's request and returns GPT model's response with streaming.

    :param message: User's message object.
    """
    telegram_id = message.from_user.id
    language = get_language_of_single_user(telegram_id)
    bot_message = await message.reply(get_loading_message(language), parse_mode=None)
    context = {
        "telegram_id": telegram_id,
        "text": message.text,
        "language": language,
        "bot_message_id": bot_message.message_id,
    }
    await generate_gpt_response(context)
