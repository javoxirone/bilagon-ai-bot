import os

from aiogram.types import Message

from config.integrations import document_parser, bot, status_manager
from services.api.openai_api_services import get_text_response_with_context
from services.api.telegram_api_services import download_document_file
from services.database.conversation_database_services import save_conversation, get_conversation_list
from services.database.user_database_services import get_user_language
from services.handler.text_handler_services import process_streaming_response
from tasks import delete_handled_file


@status_manager.status_update_decorator({
    "start": "Processing your document...",
    "download": "Downloading the document...",
    "parse": "Parsing the content...",
    "final_request": "Preparing the final request...",
    "generate": "Generating the response..."
})
async def handle_document(message: Message, status_context: dict) -> None:
    """Handle document processing with automated status updates."""
    await status_context["update_status"]("start")
    telegram_id = message.from_user.id
    document = message.document
    caption = message.caption or ""
    user_language = get_user_language(telegram_id)
    full_path = None

    try:
        # Download document
        await status_context["update_status"]("download")
        full_path = await download_document_file(document)

        # Parse document
        await status_context["update_status"]("parse")
        extracted_document_content = document_parser.parse_document(full_path)

        await status_context["update_status"]("final_request")
        # Build the message with extracted content
        final_request_message = f"\"{extracted_document_content}\"\n\nThis is a content that was extracted from the document.\n\n{caption}"

        # Save conversation and get context
        save_conversation(telegram_id, "user", final_request_message)
        conversation_list = get_conversation_list(telegram_id)

        # Generate response
        await status_context["update_status"]("generate")
        response_generator = get_text_response_with_context(conversation_list)
        assistant_response = await process_streaming_response(
            message,
            status_context["status_message_id"],
            response_generator,
            user_language
        )

        # Save assistant response
        save_conversation(telegram_id, "assistant", assistant_response)

    finally:
        # Clean up temporary files
        if full_path and os.path.exists(full_path):
            delete_handled_file.delay(full_path)
