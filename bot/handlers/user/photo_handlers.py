from aiogram import Bot
from aiogram.types import Message
from services.api.openai import get_text_response_with_context
from services.database.conversation import save_conversation, get_conversation_list
from services.database.user import get_user_language
from utils.handler.image_to_text_utils import handle_message_photo
from utils.handler.response_generation_utils import process_streaming_response


async def handle_photo(message: Message, bot: Bot) -> None:
    # Send a new message instead of trying to edit the original user's message
    status_message = await message.reply("Handling the media...")
    status_message_id = status_message.message_id
    telegram_id = message.from_user.id
    user_language = get_user_language(telegram_id)
    message_photo = message.photo[-1]
    message_caption = message.caption
    path = f"media/photos/{message_photo.file_id}.jpg"

    # Update our bot's status message instead of the original message
    await bot.edit_message_text(chat_id=telegram_id, message_id=status_message_id, text="Downloading the media...")
    await bot.download(message_photo, destination=path)

    await bot.edit_message_text(chat_id=telegram_id, message_id=status_message_id, text="Extracting the text...")
    extracted_text = handle_message_photo(path, user_language)

    await bot.edit_message_text(chat_id=telegram_id, message_id=status_message_id,
                                text="Preparing the final request message...")
    final_request_message = (
        f'"{extracted_text}"\nThis is text that is extracted from an image\n\n' + message_caption if message_caption else extracted_text
    )

    await bot.edit_message_text(chat_id=telegram_id, message_id=status_message_id, text="Generating the response...")
    save_conversation(telegram_id, "user", final_request_message)
    conversation_list = get_conversation_list(telegram_id)
    response_generator = get_text_response_with_context(conversation_list)

    # Pass the status_message_id instead of original_message_id
    assistant_response_message = await process_streaming_response(message, status_message_id, response_generator,
                                                                  user_language)
    save_conversation(telegram_id, "assistant", assistant_response_message)
