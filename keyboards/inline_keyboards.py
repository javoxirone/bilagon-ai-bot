from aiogram import types


def get_lang_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(
                text="🇺🇿 O'zbekcha", callback_data='lang_uz'
            )
        ],
        [
            types.InlineKeyboardButton(
                text="🇷🇺 Русский", callback_data='lang_ru'
            )
        ],
        [
            types.InlineKeyboardButton(
                text="🇺🇸 English", callback_data='lang_en'
            )
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_new_chat_keyboard(lang):
    buttons = {
        "uz": types.InlineKeyboardButton(
            text="💬 Yangi suhbat 💬", callback_data='new_chat'
        ),
        "ru": types.InlineKeyboardButton(
            text="💬 Новый разговор 💬", callback_data='new_chat'
        ),
        "en": types.InlineKeyboardButton(
            text="💬 New Chat 💬", callback_data='new_chat'
        ),
    }
    button = [[buttons[lang]]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=button)
    return keyboard


def get_chat_mode_keyboard(lang):
    regular_chat_buttons = {
        "uz": types.InlineKeyboardButton(
            text="Odatiy", callback_data='regular_chat'
        ),
        "ru": types.InlineKeyboardButton(
            text="Обычный", callback_data='regular_chat'
        ),
        "en": types.InlineKeyboardButton(
            text="Regular", callback_data='regular_chat'
        ),
    }
    scientific_chat_buttons = {
        "uz": types.InlineKeyboardButton(
            text="Ilmiy", callback_data='scientific_chat'
        ),
        "ru": types.InlineKeyboardButton(
            text="Научный", callback_data='scientific_chat'
        ),
        "en": types.InlineKeyboardButton(
            text="Scientific", callback_data='scientific_chat'
        ),
    }
    button = [[regular_chat_buttons[lang], scientific_chat_buttons[lang]]]
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
