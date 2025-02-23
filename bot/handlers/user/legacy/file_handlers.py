from aiogram.types import Message
from services.file import recognize_function_by_file_extension
from services.gpt import handle_gpt_response
from aiogram import Bot
from tasks import delete_handled_file


async def document_handler(message: Message, bot: Bot) -> None:
    """
    This handlers gets message and bot objects as arguments and gets attached file with caption,
    then downloads the file and reads the content (if file size is less than 1mb).
    Finally, the content of the document and caption written in one context are conveyed the gpt.

    :param message: Message object.
    :param bot: Bot object.
    """
    # DOCX, TXT, PDF
    document = message.document
    if document.file_size > 3_000_000:
        await message.answer("Document size sould be less than 1mb!")
        return

    telegram_id = message.from_user.id
    file_name = document.file_name
    file_extension = file_name.split(".")[-1].lower()
    file_id = document.file_id
    caption = message.caption

    path = f"media/documents/{file_id}.{file_extension}"
    await bot.download(file_id, destination=path)

    file_content = recognize_function_by_file_extension(path, file_extension)

    await handle_gpt_response(
        telegram_id,
        [
            message.message_id,
            f"{file_extension} file content: \n{file_content}\n\n{caption}",
        ],
    )

    delete_handled_file.delay(path)
