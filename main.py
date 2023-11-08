import re
import time

from dotenv import load_dotenv
from gpt import OpenAIAPI
from utils import initialize_user, get_user_language_by_telegram_id

load_dotenv()
import asyncio
import os
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.filters import Command
import logging
from db import UserDatabase
from message_handlers import get_start_command_message, get_language_command_message, get_user_prompt_message, \
    get_new_chat_message, get_help_command_message, get_examples_command_message, get_token_update_message, \
    get_no_tokens_message, get_settings_command_message, \
    get_premium_requests_num_message, get_settings_command_premium_user_message, get_donate_command_message
from keyboards import get_lang_keyboard, get_new_chat_keyboard, get_gpt3_payment_keyboard

TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=TOKEN, parse_mode=ParseMode.MARKDOWN)
dp = Dispatcher()
gpt = OpenAIAPI()


@dp.message(Command('start'))
async def command_start_handler(message: Message) -> None:
    is_registered_user = await initialize_user(message)
    if is_registered_user:
        db = UserDatabase()
        user = db.get_user_by_telegram_id(message.from_user.id)
        db.close()
        await message.answer(get_start_command_message(user["language"]))


@dp.message(Command('help'))
async def command_help_handler(message: Message) -> None:
    is_registered_user = await initialize_user(message)
    if is_registered_user:
        telegram_id = message.from_user.id
        db = UserDatabase()
        user = db.get_user_by_telegram_id(telegram_id)
        db.close()
        language = user["language"]
        await message.answer(get_help_command_message(language), parse_mode=ParseMode.HTML)


@dp.message(Command('settings'))
async def command_settings_handler(message: Message) -> None:
    is_registered_user = await initialize_user(message)
    if is_registered_user:
        telegram_id = message.from_user.id
        db = UserDatabase()
        user = db.get_user_by_telegram_id(telegram_id)
        db.close()
        # tariff = "Premium" if user['has_premium_gpt3'] else "Free"
        tariff = "-"
        # requests_num = get_premium_requests_num_message(user['language']) if user['has_premium_gpt3'] else user['gpt3_requests_num']
        requests_num = get_premium_requests_num_message(user['language'])
        # expiration_date = user['gpt3_requests_expire_datetime']
        expiration_date = "-"
        language = user['language']
        if user['has_premium_gpt3']:
            await message.answer(get_settings_command_premium_user_message(tariff, requests_num, expiration_date, language), parse_mode=ParseMode.HTML)
            return
        await message.answer(get_settings_command_message(tariff, requests_num, expiration_date, language),
                             parse_mode=ParseMode.HTML)


@dp.message(Command('language'))
async def command_language_handler(message: Message) -> None:
    is_registered_user = await initialize_user(message)
    if is_registered_user:
        telegram_id = message.from_user.id
        db = UserDatabase()
        user = db.get_user_by_telegram_id(telegram_id)
        db.close()
        await message.answer(get_language_command_message(user["language"]), reply_markup=get_lang_keyboard())


@dp.message(Command('examples'))
async def command_examples_handler(message: Message) -> None:
    is_registered_user = await initialize_user(message)
    if is_registered_user:
        telegram_id = message.from_user.id
        db = UserDatabase()
        user = db.get_user_by_telegram_id(telegram_id)
        db.close()
        language = user["language"]
        await message.answer(get_examples_command_message(language))


@dp.message(Command('donate'))
async def command_donate_handler(message: Message) -> None:
    is_registered_user = await initialize_user(message)
    if is_registered_user:
        telegram_id = message.from_user.id
        language = get_user_language_by_telegram_id(telegram_id)
        return message.answer(get_donate_command_message(language), parse_mode=ParseMode.HTML)

@dp.callback_query(lambda c: c.data == 'uz')
async def process_callback_uz_lang(callback_query: CallbackQuery):

    telegram_id = callback_query.from_user.id
    db = UserDatabase()
    db.change_language(telegram_id, callback_query.data)
    db.close()

    await bot.delete_message(telegram_id, callback_query.message.message_id)
    await bot.send_message(telegram_id, "O'zbek tili tanlandi, savolingizga javob berishga tayyorman 😊")


@dp.callback_query(lambda c: c.data == 'ru')
async def process_callback_ru_lang(callback_query: CallbackQuery):
    telegram_id = callback_query.from_user.id
    db = UserDatabase()
    db.change_language(telegram_id, callback_query.data)
    db.close()

    await bot.delete_message(telegram_id, callback_query.message.message_id)
    await bot.send_message(telegram_id, "Выбран русский язык, я готов ответить на ваши вопросы 😊")


@dp.callback_query(lambda c: c.data == 'en')
async def process_callback_en_lang(callback_query: CallbackQuery):
    telegram_id = callback_query.from_user.id
    db = UserDatabase()
    db.change_language(telegram_id, callback_query.data)
    db.close()

    await bot.delete_message(telegram_id, callback_query.message.message_id)
    await bot.send_message(telegram_id, "English language selected, I am ready to answer your questions 😊")


@dp.callback_query(lambda c: c.data == 'new_chat')
async def process_callback_new_chat(callback_query: CallbackQuery):
    is_registered_user = await initialize_user(callback_query)
    if is_registered_user:
        telegram_id = callback_query.from_user.id
        db = UserDatabase()
        user = db.get_user_by_telegram_id(telegram_id)
        db.close()
        gpt.reset_chat(telegram_id)
        await bot.send_message(telegram_id, get_new_chat_message(user["language"]))


@dp.callback_query(lambda c: c.data == 'buy_premium_gpt3')
async def process_callback_buy_monthly_gpt3(callback_query: CallbackQuery):
    is_registered_user = await initialize_user(callback_query)
    if is_registered_user:
        pass


async def safe_edit_message_text(
    message: types.Message,
    text: str,
    parse_mode: str = None,
    disable_web_page_preview: bool = False,
    reply_markup: types.InlineKeyboardMarkup = None,
    disable_notification: bool = False
):
    try:
        await message.edit_text(
            text,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
            reply_markup=reply_markup,
            disable_notification=disable_notification
        )
    except Exception as e:
        logging.error(f"Failed to edit message text: {e}")

import openai
@dp.message()
async def message_handler(message: Message) -> None:
    is_registered_user = await initialize_user(message)
    if is_registered_user:
        telegram_id = message.from_user.id
        db = UserDatabase()
        user = db.get_user_by_telegram_id(telegram_id)
        db.close()
        language = user["language"]
        bot_message = await message.reply(get_user_prompt_message(language), parse_mode=None)

        openai.api_key = os.getenv("OPENAI_API")
        result = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            max_tokens=2000,
            messages=[
                {
                    "role": "user",
                    "content": message.text
                }
            ],
            stream=True  # Add this optional property.
        )
        text = ""
        counter = 0
        for chunk in result:

            text += chunk.choices[0].delta.get("content", "")
            if counter >= 15:
                await bot.edit_message_text(text, telegram_id, bot_message.message_id, parse_mode=None)
                counter = 0
            counter += 1
        await bot.edit_message_text(text, telegram_id, bot_message.message_id, parse_mode=ParseMode.MARKDOWN, reply_markup=get_new_chat_keyboard(language))
        #     print(
        #         chunk.choices[0].delta.get("content", ""),
        #         end="",
        #         flush=True
        #     )
        # print()

        # if not user['has_premium_gpt3'] and user['gpt3_requests_num'] > 0:
        #     tokens = user['gpt3_requests_num'] - 1
        #     db = UserDatabase()
        #     db.update_tokens(telegram_id, 'gpt3', tokens)
        #     db.close()
        # if not user['has_premium_gpt3'] and user['gpt3_requests_num'] <= 0:
        #     await message.answer(get_no_tokens_message(language), reply_markup=get_gpt3_payment_keyboard(language))
        #     return

        # result = gpt.generate_response(telegram_id, message.text, max_tokens=2000)
        # for generated_text in result:
        #     print(generated_text)
        #     await message.reply(generated_text, reply_markup=get_new_chat_keyboard(language))
        #     await bot.edit_message_text(chat_id=telegram_id, message_id=message.message_id + 2, text=generated_text)

        # while True:
        #     # Generate a response to the user's message
        #     generated_text, _ = gpt.generate_response(telegram_id, message.text, max_tokens=2000)
        #
        #     if generated_text:
        #         print("Assistant:", generated_text)  # Replace this with your method of sending responses to the user
        #         await message.reply(generated_text, reply_markup=get_new_chat_keyboard(language))
        #         await bot.edit_message_text(chat_id=telegram_id, message_id=message.message_id+2, text=generated_text)


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot_inner = Bot(TOKEN, parse_mode=ParseMode.MARKDOWN)
    # And the run events dispatching
    await dp.start_polling(bot_inner)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())