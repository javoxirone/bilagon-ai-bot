from database.user import User
from keyboards.inline_keyboards import get_lang_keyboard


def initialize_user(func):
    async def wrapper(message):
        user = message.from_user
        telegram_id = user.id
        username = user.username
        first_name = user.first_name
        last_name = user.last_name

        db = User()
        print(db.get_user_by_telegram_id(telegram_id))
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
        await func(message)
        db.close()
    return wrapper