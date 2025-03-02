from aiogram.types import Message
from services.api.openai_api_services import get_text_response_with_context
from services.database.conversation_database_services import save_conversation, get_conversation_list
from services.database.user_database_services import get_user_language
from services.handler.text_handler_services import process_streaming_response


async def handle_saved_conversation(telegram_id: int, user_request_message: str, status_message_id: int) -> None:
    user_language = get_user_language(telegram_id)
    save_conversation(telegram_id=telegram_id, role="user", content=user_request_message)
    conversation_list = get_conversation_list(telegram_id)
    response_generator = get_text_response_with_context(conversation_list, user_language)
    assistant_response_message = await process_streaming_response(
        telegram_id, status_message_id, response_generator, user_language
    )
    save_conversation(telegram_id=telegram_id, role="assistant", content=assistant_response_message)
