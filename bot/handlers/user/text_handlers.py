from aiogram.types import Message

from config.integrations import status_manager
from services.api.openai_api_services import get_text_response_with_context
from services.database.conversation_database_services import save_conversation, get_conversation_list
from services.database.user_database_services import get_user_language
from services.handler.text_handler_services import process_streaming_response


@status_manager.status_update_decorator({
    "start": "Processing your text message...",
    "generate": "Generating the response..."
})
async def handle_message_with_context(message: Message, status_context: dict) -> None:
    """Main handler for incoming messages with conversation context."""
    await status_context["update_status"]("start")
    telegram_id = message.chat.id
    user_request_message = message.text

    save_conversation(telegram_id=telegram_id, role="user", content=user_request_message)
    conversation_list = get_conversation_list(telegram_id)

    await status_context["update_status"]("generate")
    response_generator = get_text_response_with_context(conversation_list)
    user_language = get_user_language(telegram_id)
    assistant_response_message = await process_streaming_response(
        message, status_context['status_message_id'], response_generator, user_language
    )

    save_conversation(telegram_id=telegram_id, role="assistant", content=assistant_response_message)
