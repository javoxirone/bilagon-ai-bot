from aiogram import types


def build_suggested_questions_keyboard(options: list) -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text=option)] for option in options],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard
