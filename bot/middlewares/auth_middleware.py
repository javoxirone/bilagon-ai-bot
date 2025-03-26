from typing import Callable, Dict, Any, Awaitable
from aiogram import Bot
from aiogram.types import Update, User as UserType, CallbackQuery
from keyboards.inline_keyboards import get_intro_lang_keyboard
from services.database.user_database_services import user_exists, update_user_language
from services.database.user_database_services import add_new_user


async def auth_middleware(
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
) -> Any:
    try:
        user: UserType = data.get("event_from_user")
        bot: Bot = data.get("bot")

        # Validate required data
        if not user or not bot:
            print("Missing user or bot in middleware data")
            return None

        # Check if user exists
        if not user_exists(user.id):
            # Handle language selection for new users
            if isinstance(event.event, CallbackQuery) and event.event.data.startswith('intro_lang_'):
                user_language = event.event.data.split('_')[1]

                # Add user with selected language
                add_new_user(user)
                update_user_language(user.id, user_language)

                return await handler(event, data)

            # Send welcome messages with language selection
            welcome_messages = {
                'uz': "🇺🇿 \nAssalomu alaykum, men Bilag'onman. Har qanday savolingizga javob berishga harakat qilaman!",
                'ru': "🇷🇺 \nЗдравствуйте, я Bilag'on. Я постараюсь ответить на все ваши вопросы!",
                'en': "🇺🇸 \nHello, I am Bilag'on. I will try to answer all your questions!"
            }
            # Send welcome messages in multiple languages
            for lang, message in welcome_messages.items():
                await bot.send_message(user.id, message)

            # Send language selection message
            await bot.send_message(
                user.id,
                "🗣",
                reply_markup=get_intro_lang_keyboard()
            )

            return None

        # Proceed with the original handler for existing users
        return await handler(event, data)

    except Exception as e:
        print(f"Error in auth middleware: {e}")
        return None
