from aiogram import types
from aiogram.types import KeyboardButton


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


def get_message_keyboard(lang):
    new_chat_buttons = {
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
    suggestion_buttons = {
        "uz": types.InlineKeyboardButton(
            text="💡 Takliflar 💡", callback_data='suggestions'
        ),
        "ru": types.InlineKeyboardButton(
            text="💡 Предложения 💡", callback_data='suggestions'
        ),
        "en": types.InlineKeyboardButton(
            text="💡 Suggestions 💡", callback_data='suggestions'
        ),
    }

    button = [[new_chat_buttons[lang]], [suggestion_buttons[lang]]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=button)
    return keyboard


def get_incognito_message_keyboard(lang):
    context_buttons = {
        "uz": types.InlineKeyboardButton(
            text="💾 Kontekstni yoqish 💾", callback_data='activate_context'
        ),
        "ru": types.InlineKeyboardButton(
            text="💾 Включить контекст 💾", callback_data='activate_context'
        ),
        "en": types.InlineKeyboardButton(
            text="💾 Activate context 💾", callback_data='activate_context'
        ),
    }
    button = [[context_buttons[lang]]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=button)
    return keyboard


def get_settings_keyboard(lang):
    conversation_mode_buttons = {
        "uz": types.InlineKeyboardButton(
            text="Suhbat rejimini almashtirish", callback_data='toggle_saved_conversation_mode'
        ),
        "ru": types.InlineKeyboardButton(
            text="Переключить режим разговора", callback_data='toggle_saved_conversation_mode'
        ),
        "en": types.InlineKeyboardButton(
            text="Switch conversation mode", callback_data='toggle_saved_conversation_mode'
        ),
    }
    switch_language_keyboard = {
        "uz": types.InlineKeyboardButton(
            text="Botning tilini almashtirish", callback_data='switch_language'
        ),
        "ru": types.InlineKeyboardButton(
            text="Переключить язык бота", callback_data='switch_language'
        ),
        "en": types.InlineKeyboardButton(
            text="Switch bot language", callback_data='switch_language'
        ),
    }
    switch_model_keyboard = {
        "uz": types.InlineKeyboardButton(
            text="Suniy idrok modelini almashtirish", callback_data='switch_model'
        ),
        "ru": types.InlineKeyboardButton(
            text="Выбрать другую модель ИИ", callback_data='switch_model'
        ),
        "en": types.InlineKeyboardButton(
            text="Switch AI model", callback_data='switch_model'
        ),
    }
    new_chat_buttons = {
        "uz": types.InlineKeyboardButton(
            text="Suhbat tarixini tozalash", callback_data='new_chat'
        ),
        "ru": types.InlineKeyboardButton(
            text="Очистить историю разговора", callback_data='new_chat'
        ),
        "en": types.InlineKeyboardButton(
            text="Clear conversation history", callback_data='new_chat'
        ),
    }
    button = [[conversation_mode_buttons[lang]], [switch_language_keyboard[lang]], [switch_model_keyboard[lang]],
              [new_chat_buttons[lang]]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=button)
    return keyboard


def build_models_keyboard(models, selected_model) -> types.InlineKeyboardMarkup:
    """
    Generate an inline keyboard from a list of model names.

    :param models: List of model names to create buttons for.
    :type models: list[str]

    :param selected_model: Selected model name.
    :type selected_model: str

    :return: Inline keyboard markup
    :rtype: types.InlineKeyboardMarkup
    """
    buttons = [
        [types.InlineKeyboardButton(text=model + " ✔️" if model == selected_model else model, callback_data=model)]
        for model in models
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
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
