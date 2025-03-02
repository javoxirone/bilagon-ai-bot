import os
import logging
import pytesseract
from aiogram import Bot
from aiogram.types import Message
from PIL import Image
from config.integrations import status_manager
from services.database.user_database_services import get_user_language
from services.handler.common import handle_saved_conversation
from services.handler.photo_handler_services import handle_message_photo
from templates.message_templates import get_processing_photo_message, get_downloading_photo_message, \
    get_extracting_text_from_photo_message, get_final_request_message, get_generating_response_message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@status_manager.status_update_decorator()
async def handle_photo(message: Message, bot: Bot, status_context: dict) -> None:
    """Handle photo messages with OCR and send AI-generated responses."""
    # Initial setup
    user_language = get_user_language(message.from_user.id)
    message_caption = message.caption or ""
    await status_context["update_status"](get_processing_photo_message(user_language))
    try:
        # Create directory and set path
        os.makedirs("media/photos", exist_ok=True)
        photo = message.photo[-1]  # Get the highest quality photo
        path = f"media/photos/{photo.file_id}.jpg"

        # Download image
        await status_context["update_status"](get_downloading_photo_message(user_language))

        await bot.download(photo, destination=path)

        # Extract text using OCR
        await status_context["update_status"](get_extracting_text_from_photo_message(user_language))

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
        await status_context["update_status"](get_final_request_message(user_language))

        # Final text processing
        final_text = extracted_text.strip() if extracted_text.strip() else ""
        final_request_message = f'"{final_text}"\n\nThis is text extracted from an image.'

        if message_caption:
            final_request_message += f"\n\n{message_caption}"

        # Generate response
        await status_context["update_status"](get_generating_response_message(user_language))

        await handle_saved_conversation(message.from_user.id, final_request_message,
                                        status_context['status_message_id'])

    except Exception as e:
        logger.error(f"Error processing photo: {str(e)}", exc_info=True)
        await message.reply(
            "Sorry, I encountered an error while processing your image. Please try again or send a clearer image."
        )
