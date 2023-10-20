from aiogram import types


def get_lang_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(
                text="🇺🇿 O'zbekcha", callback_data='uz'
            )
        ],
        [
            types.InlineKeyboardButton(
                text="🇷🇺 Русский", callback_data='ru'
            )
        ],
        [
            types.InlineKeyboardButton(
                text="🇺🇸 English", callback_data='en'
            )
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_new_chat_keyboard(lang):
    buttons = {
        "uz":types.InlineKeyboardButton(
                text="Yangi suhbat 🔄", callback_data='new_chat'
            ),
        "ru": types.InlineKeyboardButton(
                text="Новый разговор 🔄", callback_data='new_chat'
            ),
        "en": types.InlineKeyboardButton(
                text="New Chat 🔄", callback_data='new_chat'
            ),
    }
    button = [[buttons[lang]]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=button)
    return keyboard


def get_gpt3_payment_keyboard(lang):
    buttons = {
        "uz": types.InlineKeyboardButton(
                text="🔥 Premium tarifga o'tish 🔥", callback_data='buy_premium_gpt3'
            ),
        "ru": types.InlineKeyboardButton(
                text="🔥 Перейти на тариф Премиум 🔥", callback_data='buy_premium_gpt3'
            ),
        "en": types.InlineKeyboardButton(
                text="🔥 Switch to Premium 🔥", callback_data='buy_premium_gpt3'
            ),
    }
    button = [[buttons[lang]]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=button)
    return keyboard