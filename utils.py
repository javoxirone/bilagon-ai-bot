from datetime import datetime

from aiogram.types import Message
from db import UserDatabase
from keyboards import get_lang_keyboard


async def initialize_user(message: Message) -> bool:
    telegram_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    db = UserDatabase()

    if not db.user_exists(telegram_id):
        await message.answer(
            "🇺🇿\nAssalomu alaykum, men Bilag'onman. Har qanday savolingizga javob berishga harakat qilaman 🤓\n\n"
            "🇷🇺\nЗдравствуйте, я Bilag'on. Я постораюсь ответить на все ваши вопросы 🤓\n\n"
            "🇺🇸\nHello, I am Bilag'on. I will try to answer all your questions 🤓")
        await message.answer(
            "🇺🇿 Savol berish uchun, oldin tilni tanlang:\n"
            "🇷🇺 Что-бы задать вопрос, сначала выберите язык:\n"
            "🇺🇸 To ask a question, choose the language first:", reply_markup=get_lang_keyboard())
        db.add_user(telegram_id, username, first_name, last_name, '')
        db.close()
        return False
    return True


def format_datetime(dt):
    if dt:
        return datetime.strptime(dt.split(".")[0], '%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S %d.%m.%Y')
    return None