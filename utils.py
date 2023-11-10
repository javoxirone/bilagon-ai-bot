import json
import os
from datetime import datetime

from aiogram.types import Message, CallbackQuery
from db import UserDatabase
from keyboards import get_lang_keyboard
import time
import random
import hmac
import hashlib
import base64


def get_auth_headers(request_data):
    request_json = json.dumps(request_data, separators=(',', ':'), ensure_ascii=False)
    signature = calculate_signature(request_json)

    headers = {
        "X-Auth": os.getenv("MERCHANT_ID"),
        "X-Signature": signature,
        "Content-Type": "application/json; charset=utf-8",
    }

    return headers


def calculate_signature(data):
    # Use HMAC-SHA1 to calculate the signature
    hmac_obj = hmac.new(os.getenv("SECRET_KEY").encode('utf-8'), data.encode('utf-8'), hashlib.sha1)
    signature = base64.b64encode(hmac_obj.digest()).decode('utf-8')
    return signature


def generate_unique_payment_id():
    # Generate a unique payment ID based on current timestamp and a random number
    timestamp = int(time.time())
    random_number = random.randint(1000, 9999)  # You can adjust the range as needed
    payment_id = f"{timestamp}{random_number}"
    return payment_id


async def initialize_user(message: Message | CallbackQuery) -> bool:
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


def get_user_language_by_telegram_id(telegram_id: int) -> str:
    db = UserDatabase()
    user = db.get_user_by_telegram_id(telegram_id)
    db.close()
    language = user["language"]
    return language