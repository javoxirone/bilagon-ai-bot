
from openai import error
from aiogram.types import Message
from database.conversation import Conversation
from database.user import User
from templates.message_templates import (
    get_loading_message,
    get_openai_error_message,
    get_bot_error_message,
)
from config.integrations import bot, gpt
from aiogram.enums import ParseMode
from keyboards.inline_keyboards import get_new_chat_keyboard
from services.utils import (
    initialize_user,
)

async def message_handler(message: Message) -> None:
    text = ""
    is_registered_user = await initialize_user(message)
    if is_registered_user:
        telegram_id = message.from_user.id
        user_db = User()
        user = user_db.get_user_by_telegram_id(telegram_id)
        user_db.close()
        language = user["language"]
        bot_message = await message.reply(get_loading_message(language), parse_mode=None)

        try:
            conversation_db = Conversation()
            conversation_db.add_conversation(telegram_id, "user", message.text)
            messages = conversation_db.get_conversations_by_telegram_id(telegram_id)
            print(messages)
            conversation_db.close()

            result = gpt.generate_response(max_tokens=2000, messages=messages)
            chunks = []
            counter = 0
            for chunk in result:
                chunks.append(chunk.choices[0].delta.get("content", ""))
                counter += 1
                if counter >= 15:
                    await bot.edit_message_text("".join(chunks) + " ▌", telegram_id, bot_message.message_id,
                                                parse_mode=None)
                    counter = 0

            text = "".join(chunks)
            await bot.edit_message_text(text, telegram_id, bot_message.message_id, parse_mode=ParseMode.MARKDOWN,
                                        reply_markup=get_new_chat_keyboard(language))
            conversation_db = Conversation()
            conversation_db.add_conversation(telegram_id, "assistant", text)
            conversation_db.close()

        except error.OpenAIError as e:
            print(e)
            await bot.edit_message_text(get_openai_error_message(language), telegram_id, bot_message.message_id,
                                        parse_mode=ParseMode.HTML)
        except Exception as e:
            print(e)
            if text:
                await bot.edit_message_text(text, telegram_id, bot_message.message_id, parse_mode=ParseMode.MARKDOWN,
                                            reply_markup=get_new_chat_keyboard(language))
                return
            await bot.edit_message_text(get_bot_error_message(language), telegram_id, bot_message.message_id,
                                        parse_mode=ParseMode.HTML, reply_markup=get_new_chat_keyboard(language))


