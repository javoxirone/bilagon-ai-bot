import pytesseract
from PIL import Image
from aiogram.types import Message
from aiogram import Bot
from bot.handlers.message_handlers import handle_gpt_response
from tasks import delete_handled_file


# TODO: clear out the code, break down into utility functions
async def image_handler(message: Message, bot: Bot) -> None:
    telegram_id = message.from_user.id
    photo = message.photo[-1]
    message_text = message.caption
    path = f"media/images/{photo.file_id}.jpg"
    await bot.download(photo, destination=path)

    extracted_text = extract_text_from_bytes(path)
    # Deleting already used image
    delete_handled_file.delay(path)
    result_text = (
        f'"{extracted_text}"\n\n' + message_text if message_text else extracted_text
    )
    await handle_gpt_response(telegram_id, [message.message_id, result_text])


def extract_text_from_bytes(image_path: str) -> str:
    img = Image.open(image_path)
    extracted_text = pytesseract.image_to_string(img)
    return extracted_text
