import asyncio
import os
import sys
import logging
from openai import error
from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.filters import Command
from db import UserDatabase
from message_handlers import get_start_command_message, get_language_command_message, get_loading_message, \
    get_new_chat_message, get_help_command_message, get_examples_command_message, get_settings_command_message, \
    get_premium_requests_num_message, get_donate_command_message, get_openai_error_message, get_bot_error_message
from keyboards import get_lang_keyboard, get_new_chat_keyboard
from dotenv import load_dotenv
from gpt import OpenAIAPI
from utils import initialize_user, get_user_language_by_telegram_id
from aiogram import F

load_dotenv()
gpt = OpenAIAPI()

TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=TOKEN, parse_mode=ParseMode.MARKDOWN)
dp = Dispatcher()


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
        tariff = "-"
        requests_num = get_premium_requests_num_message(user['language'])
        expiration_date = "-"
        language = user['language']
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
        await message.answer(get_donate_command_message(language), parse_mode=ParseMode.HTML)


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


@dp.message(F.text)
async def message_handler(message: Message) -> None:
    is_registered_user = await initialize_user(message)
    if is_registered_user:
        telegram_id = message.from_user.id
        db = UserDatabase()
        user = db.get_user_by_telegram_id(telegram_id)
        db.close()
        language = user["language"]
        bot_message = await message.reply(get_loading_message(language), parse_mode=None)
        try:
            messages = gpt.user_histories.get(telegram_id, [])
            messages.append({"role": "user", "content": message.text})
            result = gpt.generate_response(max_tokens=2000, messages=messages)
            text = ""
            counter = 0
            for chunk in result:

                text += chunk.choices[0].delta.get("content", "")
                if counter >= 30:
                    await bot.edit_message_text(text + " ▌", telegram_id, bot_message.message_id, parse_mode=None)
                    counter = 0
                counter += 1

            gpt.update_user_histories(telegram_id, message.text, text)
            await bot.edit_message_text(text, telegram_id, bot_message.message_id, parse_mode=ParseMode.MARKDOWN,
                                        reply_markup=get_new_chat_keyboard(language))
        except error.OpenAIError as e:
            print(e)
            await bot.edit_message_text(get_openai_error_message(language), telegram_id, bot_message.message_id,
                                        parse_mode=ParseMode.HTML)
        except Exception as e:
            print(e)
            await bot.edit_message_text(get_bot_error_message(language), telegram_id, bot_message.message_id,
                                        parse_mode=ParseMode.HTML, reply_markup=get_new_chat_keyboard(language))


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
