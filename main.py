from dotenv import load_dotenv

from gpt import OpenAIAPI

load_dotenv()
import asyncio
import os
import sys
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.filters import Command
import logging
from db import UserDatabase
from message_handlers import get_start_command_message, get_language_command_message, get_user_prompt_message, \
    get_new_chat_message, get_help_command_message, get_examples_command_message, get_token_update_message, \
    get_no_tokens_message, get_gpt3_payment_successful_message
from keyboards import get_lang_keyboard, get_new_chat_keyboard, get_gpt3_payment_keyboard

TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=TOKEN, parse_mode=ParseMode.MARKDOWN)
dp = Dispatcher()
gpt = OpenAIAPI()


# Function to update user tokens
async def update_tokens():
    db = UserDatabase()
    users = db.get_all_users()
    for user in users:
        telegram_id, tokens, language = user['telegram_id'], user['gpt3_token'], user['language']
        db.update_tokens(telegram_id, 'gpt3', 5)
        if not db.has_premium_subscription(telegram_id, 'gpt3'):
            await bot.send_message(telegram_id, get_token_update_message(language))
    db.close()


# Schedule the update_tokens function to run once a day
async def scheduler():
    while True:
        await update_tokens()
        await asyncio.sleep(86400)  # 86400 seconds = 24 hours


@dp.message(Command('start'))
async def command_start_handler(message: Message) -> None:
    telegram_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    db = UserDatabase()
    if not db.user_exists(telegram_id):
        await message.answer("🇺🇿\nAssalomu alaykum, men Bilag'onman. Har qanday savolingizga javob berishga harakat qilaman 🤓\n\n"
                             "🇷🇺\nЗдравствуйте, я Bilag'on. Я постораюсь ответить на все ваши вопросы 🤓\n\n"
                             "🇺🇸\nHello, I am Bilag'on. I will try to answer all your questions 🤓")
        await message.answer(
            "🇺🇿 Savol berish uchun, oldin tilni tanlang:\n"
            "🇷🇺 Что-бы задать вопрос, сначала выберите язык:\n"
            "🇺🇸 To ask a question, choose the language first:", reply_markup=get_lang_keyboard())
        db.add_user(telegram_id, username, first_name, last_name, '')
        db.close()
        return
    user = db.get_user_by_telegram_id(telegram_id)
    await message.answer(get_start_command_message(user["language"]))


@dp.message(Command('help'))
async def command_help_handler(message: Message) -> None:
    telegram_id = message.from_user.id
    db = UserDatabase()
    user = db.get_user_by_telegram_id(telegram_id)
    db.close()
    language = user["language"]
    await message.answer(get_help_command_message(language))


@dp.message(Command('settings'))
async def command_settings_handler(message: Message) -> None:
    pass


@dp.message(Command('language'))
async def command_language_handler(message: Message) -> None:
    telegram_id = message.from_user.id
    db = UserDatabase()
    user = db.get_user_by_telegram_id(telegram_id)
    db.close()
    await message.answer(get_language_command_message(user["language"]), reply_markup=get_lang_keyboard())


@dp.message(Command('examples'))
async def command_examples_handler(message: Message) -> None:
    telegram_id = message.from_user.id
    db = UserDatabase()
    user = db.get_user_by_telegram_id(telegram_id)
    db.close()
    language = user["language"]
    await message.answer(get_examples_command_message(language))


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
    telegram_id = callback_query.from_user.id
    db = UserDatabase()
    user = db.get_user_by_telegram_id(telegram_id)
    db.close()
    gpt.reset_chat(telegram_id)
    await bot.send_message(telegram_id, get_new_chat_message(user["language"]))


@dp.callback_query(lambda c: c.data == 'buy_monthly_gpt3')
async def process_callback_buy_monthly_gpt3(callback_query: CallbackQuery):
    telegram_id = callback_query.from_user.id
    db = UserDatabase()
    db.update_subscription(telegram_id, 'premium_gpt3', 5)
    user = db.get_user_by_telegram_id(telegram_id)
    db.close()
    language = user['language']
    await bot.send_message(telegram_id, get_gpt3_payment_successful_message(language))


@dp.message()
async def message_handler(message: Message) -> None:

    telegram_id = message.from_user.id
    db = UserDatabase()
    user = db.get_user_by_telegram_id(telegram_id)
    db.close()
    language = user["language"]

    if not user['has_premium_gpt3'] and user['gpt3_token'] > 0:
        tokens = user['gpt3_token'] - 1
        db = UserDatabase()
        db.update_tokens(telegram_id, 'gpt3', tokens)
        db.close()
    if not user['has_premium_gpt3'] and user['gpt3_token'] <= 0:
        await message.answer(get_no_tokens_message(language), reply_markup=get_gpt3_payment_keyboard(language))
        return
    await message.answer(get_user_prompt_message(language))
    gpt_response_text, _ = gpt.generate_text(telegram_id, message.text, max_tokens=2000)
    print(_)
    print(gpt_response_text)
    await bot.delete_message(telegram_id, message.message_id+1)
    await message.reply(gpt_response_text, reply_markup=get_new_chat_keyboard(language))


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot_inner = Bot(TOKEN, parse_mode=ParseMode.MARKDOWN)
    # And the run events dispatching
    await dp.start_polling(bot_inner)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler())
    loop.run_forever()


