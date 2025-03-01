from aiogram import Bot
from aiogram.types import Message
from services.api.openai_api_services import get_transcription_of_audio, get_text_response_with_context
from services.api.telegram_api_services import download_voice_file
from services.database.conversation_database_services import save_conversation, get_conversation_list
from services.database.user_database_services import get_user_language
from services.handler.text_handler_services import process_streaming_response
from tasks import delete_handled_file


async def voice_message_handler(message: Message, bot: Bot) -> None:
    """Handle voice messages with speech-to-text and send AI-generated responses."""
    # Initial setup
    status_message = await message.reply("Processing your voice message...")
    status_message_id = status_message.message_id
    telegram_id = message.from_user.id
    user_language = get_user_language(telegram_id)
    message_caption = message.caption or ""

    try:
        # Download voice
        await bot.edit_message_text(
            chat_id=telegram_id,
            message_id=status_message_id,
            text="Downloading the voice message..."
        )
        full_path = await download_voice_file(message.voice)

        # Convert and transcribe the voice message
        await bot.edit_message_text(
            chat_id=telegram_id,
            message_id=status_message_id,
            text="Transcribing your voice message..."
        )
        with open(full_path, "rb") as audio_file:
            transcribed_text = get_transcription_of_audio(audio_file)
            save_conversation(telegram_id, "user", transcribed_text)
            conversation_list = get_conversation_list(telegram_id)
            await bot.edit_message_text(
                chat_id=telegram_id,
                message_id=status_message_id,
                text="Generating response..."
            )
            response_generator = get_text_response_with_context(conversation_list)
            assistant_response = await process_streaming_response(
                message, status_message_id, response_generator, user_language
            )
            save_conversation(telegram_id, "assistant", assistant_response)
        delete_handled_file.delay(full_path)
    except Exception as e:
        print(e)
