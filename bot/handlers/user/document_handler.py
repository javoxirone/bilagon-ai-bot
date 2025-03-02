import os

from aiogram.types import Message

from config.integrations import document_parser, status_manager
from services.api.openai_api_services import get_text_response_with_context
from services.api.telegram_api_services import download_document_file
from services.database.conversation_database_services import save_conversation, get_conversation_list
from services.database.user_database_services import get_user_language
from services.handler.common import handle_saved_conversation
from services.handler.text_handler_services import process_streaming_response
from tasks import delete_handled_file
from templates.message_templates import get_final_request_message, get_processing_document_message, \
    get_downloading_document_message, get_parsing_content_message, get_generating_response_message


@status_manager.status_update_decorator()
async def handle_document(message: Message, status_context: dict) -> None:
    """Handle document processing with automated status updates."""
    document = message.document
    caption = message.caption or ""
    user_language = get_user_language(message.from_user.id)
    full_path = None
    await status_context["update_status"](get_processing_document_message(user_language))

    try:
        # Download document
        await status_context["update_status"](get_downloading_document_message(user_language))
        full_path = await download_document_file(document)

        # Parse document
        await status_context["update_status"](get_parsing_content_message(user_language))
        extracted_document_content = document_parser.parse_document(full_path)

        await status_context["update_status"](get_final_request_message(user_language))
        # Build the message with extracted content
        final_request_message = f"\"{extracted_document_content}\"\n\nThis is a content that was extracted from the document.\n\n{caption}"

        await status_context["update_status"](get_generating_response_message(user_language))
        await handle_saved_conversation(message.from_user.id, final_request_message,
                                        status_context['status_message_id'])

    finally:
        # Clean up temporary files
        if full_path and os.path.exists(full_path):
            delete_handled_file.delay(full_path)
