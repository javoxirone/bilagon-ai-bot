import platform
import pytesseract
from PIL import Image
from aiogram.types import Message
from aiogram import Bot
from bot.handlers.message_handlers import handle_gpt_response
from services.utils import get_language_of_single_user
from tasks import delete_handled_file


async def image_handler(message: Message, bot: Bot) -> None:
    telegram_id = message.from_user.id
    photo = message.photo[-1]
    message_text = message.caption
    path = f"media/images/{photo.file_id}.jpg"
    await bot.download(photo, destination=path)
    lang = get_language_of_single_user(telegram_id)
    extracted_text = extract_text_from_image(path, lang)
    # Deleting already used image
    delete_handled_file.delay(path)
    result_text = (
        f'"{extracted_text}"\n\n' + message_text if message_text else extracted_text
    )
    await handle_gpt_response(telegram_id, [message.message_id, result_text])


def extract_text_from_image(image_path: str, lang: str) -> str:
    langs = "eng+rus+uzb"
    img = Image.open(image_path)
    set_tesseract_cmd()
    extracted_text = pytesseract.image_to_string(img, lang=langs)
    return extracted_text


def set_tesseract_cmd():
    if platform.system() == 'Windows':
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    elif platform.system() == 'Linux':
        pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Default path for Ubuntu
    else:
        raise EnvironmentError("Unsupported operating system. Please set the Tesseract command manually.")
