from aiogram.types import Message
from decorators.auth_decorators import initialize_user
from services.gpt_services import handle_gpt_response


@initialize_user
async def message_handler(message: Message) -> None:
    """
    Gets the user's request and returns GPT model's response with streaming.

    :param message: User's message object.
    """
    telegram_id = message.from_user.id
    await handle_gpt_response(telegram_id, [message.message_id, message.text])
