from aiogram.types import Message
from config.integrations import status_manager
from services.database.user_database_services import get_user_language
from services.handler.common import handle_saved_conversation
from templates.message_templates import get_processing_text_message, get_generating_response_message


@status_manager.status_update_decorator()
async def handle_message_with_context(message: Message, status_context: dict) -> None:
    """Main handler for incoming messages with conversation context."""
    user_language = get_user_language(message.chat.id)
    await status_context["update_status"](get_processing_text_message(user_language))
    await status_context["update_status"](get_generating_response_message(user_language))
    await handle_saved_conversation(message.from_user.id, message.text, status_context['status_message_id'])
