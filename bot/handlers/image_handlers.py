import io
import pytesseract
from PIL import Image

from aiogram.types import Message
from aiogram import Bot
from pprint import pprint


# TODO: add photo remover function
async def image_handler(message: Message, bot: Bot) -> None:
    pprint(message)
    photo = message.photo[-1]
    message_text = message.caption
    path = f"media/images/{photo.file_id}.jpg"
    await bot.download(photo, destination=path)
    await message.answer("File downloaded successfully!")
    extracted_text = extract_text_from_bytes(path)
    await message.answer(f"Extracted text from the photo:\n{extracted_text}\n\n{message_text}")


def extract_text_from_bytes(image_path:str) -> str:
    img = Image.open(image_path)
    extracted_text = pytesseract.image_to_string(img)
    return extracted_text