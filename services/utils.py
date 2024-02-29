from datetime import datetime
from aiogram.types import Message, CallbackQuery
from database.user import User
from keyboards.inline_keyboards import get_lang_keyboard


async def initialize_user(message: Message | CallbackQuery) -> bool:
    """
    This utility function gets CallbackQuery or Message and initializes user (checks if the user exists on db) and returns status.

    :param message: Message of the user.
    :return: If the user exists or not.
    """
    telegram_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    db = User()

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


def format_datetime(dt) -> None | datetime:
    """
    This utility function gets datetime as an argument and returns either None or python datetime format.

    :param dt: datetime in string format.
    :return: None or python datetime format.
    """
    if dt:
        return datetime.strptime(dt.split(".")[0], '%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S %d.%m.%Y')
    return None


def get_user_language_by_telegram_id(telegram_id: int) -> str:
    """
    This utility function gets telegram_id of the user and checks the language settings of the user.

    :param telegram_id: Unique ID of the telegram user.
    :return: Language in string format (e.g. EN, RU, UZ).
    """
    db = User()
    user = db.get_user_by_telegram_id(telegram_id)
    db.close()
    language = user["language"]
    return language