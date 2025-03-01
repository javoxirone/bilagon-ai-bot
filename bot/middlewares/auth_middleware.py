from typing import Callable, Dict, Any, Awaitable
from aiogram import Bot
from aiogram.types import Update, User as UserType, CallbackQuery
from keyboards.inline_keyboards import get_lang_keyboard
from services.database.user_database_services import get_user_language, user_exists, update_user_language
from services.database.user_database_services import add_new_user

async def auth_middleware(
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
) -> Any:
    user: UserType = data["event_from_user"]
    bot: Bot = data["bot"]
    try:
        if not user_exists(user.id):
            if isinstance(event.event, CallbackQuery) and event.event.data.startswith('lang_'):
                user_language = event.event.data.split('_')[1]
                add_new_user(user)
                update_user_language(user.id, user_language)
                return await handler(event, data)
            await bot.send_message(user.id,
                                   "🇺🇿\nAssalomu alaykum, men Bilag'onman. Har qanday savolingizga javob berishga harakat qilaman 🤓\n\n"
                                   "🇷🇺\nЗдравствуйте, я Bilag'on. Я постораюсь ответить на все ваши вопросы 🤓\n\n"
                                   "🇺🇸\nHello, I am Bilag'on. I will try to answer all your questions 🤓"
                                   )
            await bot.send_message(user.id,
                                   "🇺🇿 Savol berish uchun, oldin tilni tanlang:\n"
                                   "🇷🇺 Что-бы задать вопрос, сначала выберите язык:\n"
                                   "🇺🇸 To ask a question, choose the language first:",
                                   reply_markup=get_lang_keyboard()
                                   )
            return
        return await handler(event, data)
    except Exception as e:
        print(f"Error in auth middleware: {e}")
        return