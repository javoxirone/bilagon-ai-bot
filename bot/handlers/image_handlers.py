import io
import pytesseract
from PIL import Image

from aiogram.types import Message
from aiogram import Bot
from pprint import pprint
from bot.handlers.message_handlers import generate_gpt_response
from services.utils import get_language_of_single_user
from templates.message_templates import get_loading_message
from tasks import delete_handled_file

# TODO: clear out the code, break down into utility functions
async def image_handler(message: Message, bot: Bot) -> None:
    telegram_id = message.from_user.id
    language = get_language_of_single_user(telegram_id)
    bot_message = await message.reply(get_loading_message(language), parse_mode=None)
    photo = message.photo[-1]
    message_text = message.caption
    path = f"media/images/{photo.file_id}.jpg"
    await bot.download(photo, destination=path)

    extracted_text = extract_text_from_bytes(path)
    
    # Deleting already used image
    delete_handled_file.delay(path)
    context = {
        "telegram_id": message.from_user.id,
        "text": (
            f'"{extracted_text}"\n\n' + message_text if message_text else extracted_text
        ),
        "bot_message_id": bot_message.message_id,
        "language": language,
    }
    await generate_gpt_response(context)


def extract_text_from_bytes(image_path: str) -> str:
    img = Image.open(image_path)
    extracted_text = pytesseract.image_to_string(img)
    return extracted_text
