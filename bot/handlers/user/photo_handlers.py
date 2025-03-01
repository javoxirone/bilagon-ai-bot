import os
import logging
import pytesseract
from aiogram import Bot
from aiogram.types import Message
from PIL import Image
from services.api.openai_api_services import get_text_response_with_context
from services.database.conversation_database_services import save_conversation, get_conversation_list
from services.database.user_database_services import get_user_language
from services.handler.photo_handler_services import handle_message_photo
from services.handler.text_handler_services import process_streaming_response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def handle_photo(message: Message, bot: Bot) -> None:
    """Handle photo messages with OCR and send AI-generated responses."""
    # Initial setup
    status_message = await message.reply("Processing your image...")
    status_message_id = status_message.message_id
    telegram_id = message.from_user.id
    user_language = get_user_language(telegram_id)
    message_caption = message.caption or ""

    try:
        # Create directory and set path
        os.makedirs("media/photos", exist_ok=True)
        photo = message.photo[-1]  # Get the highest quality photo
        path = f"media/photos/{photo.file_id}.jpg"

        # Download image
        await bot.edit_message_text(
            chat_id=telegram_id,
            message_id=status_message_id,
            text="Downloading the image..."
        )

        await bot.download(photo, destination=path)

        # Extract text using OCR
        await bot.edit_message_text(
            chat_id=telegram_id,
            message_id=status_message_id,
            text="Extracting text from the photo..."
        )

        # Try primary OCR method
        try:
            extracted_text = handle_message_photo(path, user_language)
        except Exception as e:
            logger.error(f"Primary OCR failed: {str(e)}")
            # Fallback to basic OCR
            try:
                pil_image = Image.open(path)
                extracted_text = pytesseract.image_to_string(pil_image)
            except Exception as alt_e:
                logger.error(f"Alternative OCR failed: {str(alt_e)}")
                extracted_text = ""

        # Prepare final request
        await bot.edit_message_text(
            chat_id=telegram_id,
            message_id=status_message_id,
            text="Preparing the final request..."
        )

        # Final text processing
        final_text = extracted_text.strip() if extracted_text.strip() else ""
        final_request_message = f'"{final_text}"\n\nThis is text extracted from an image.'

        if message_caption:
            final_request_message += f"\n\n{message_caption}"

        # Generate response
        await bot.edit_message_text(
            chat_id=telegram_id,
            message_id=status_message_id,
            text="Generating response..."
        )

        # Save conversation and get context
        save_conversation(telegram_id, "user", final_request_message)
        conversation_list = get_conversation_list(telegram_id)

        # Get and process response
        response_generator = get_text_response_with_context(conversation_list)
        assistant_response = await process_streaming_response(
            message, status_message_id, response_generator, user_language
        )

        # Save assistant response
        save_conversation(telegram_id, "assistant", assistant_response)

    except Exception as e:
        logger.error(f"Error processing photo: {str(e)}", exc_info=True)
        await message.reply(
            "Sorry, I encountered an error while processing your image. Please try again or send a clearer image."
        )
