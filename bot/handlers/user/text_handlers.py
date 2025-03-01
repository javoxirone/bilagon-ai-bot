
from aiogram.types import Message

from services.api.openai_api_services import get_text_response_with_context
from services.database.conversation_database_services import save_conversation, get_conversation_list
from services.database.user_database_services import get_user_language
from services.handler.text_handler_services import process_streaming_response


async def handle_message_with_context(message: Message) -> None:
    """Main handler for incoming messages with conversation context."""
    telegram_id = message.chat.id
    user_request_message = message.text

    save_conversation(telegram_id=telegram_id, role="user", content=user_request_message)
    conversation_list = get_conversation_list(telegram_id)

    response_generator = get_text_response_with_context(conversation_list)
    original_message = await message.reply("Loading...")
    original_message_id = original_message.message_id
    user_language = get_user_language(telegram_id)

    assistant_response_message = await process_streaming_response(
        message, original_message_id, response_generator, user_language
    )

    save_conversation(telegram_id=telegram_id, role="assistant", content=assistant_response_message)




