from aiogram import Bot
from aiogram.types import Message

from config.integrations import status_manager
from services.api.openai_api_services import get_transcription_of_audio, get_text_response_with_context
from services.api.telegram_api_services import download_voice_file
from services.database.conversation_database_services import save_conversation, get_conversation_list
from services.database.user_database_services import get_user_language
from services.handler.common import handle_saved_conversation
from services.handler.text_handler_services import process_streaming_response
from tasks import delete_handled_file
from templates.message_templates import get_downloading_voice_message, get_transcribing_voice_message, \
    get_generating_response_message, get_processing_voice_message


@status_manager.status_update_decorator()
async def handle_voice_message(message: Message, bot: Bot, status_context: dict) -> None:
    """Handle voice messages with speech-to-text and send AI-generated responses."""
    # Initial setup
    user_language = get_user_language(message.from_user.id)
    await status_context["update_status"](get_processing_voice_message(user_language))

    try:
        # Download voice
        await status_context["update_status"](get_downloading_voice_message(user_language))
        full_path = await download_voice_file(message.voice)

        # Convert and transcribe the voice message
        await status_context["update_status"](get_transcribing_voice_message(user_language))
        with open(full_path, "rb") as audio_file:
            transcribed_text = get_transcription_of_audio(audio_file)
            await status_context["update_status"](get_generating_response_message(user_language))
            await handle_saved_conversation(message.from_user.id, transcribed_text, status_context['status_message_id'])
        delete_handled_file.delay(full_path)
    except Exception as e:
        print(e)
