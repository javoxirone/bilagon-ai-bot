from aiogram.types import Message
from services.legacy.gpt import handle_gpt_response


async def message_handler(message: Message) -> None:
    """
    Gets the user's request and returns GPT model's response with streaming.

    :param message: User's message object.
    """
    telegram_id = message.from_user.id
    await handle_gpt_response(telegram_id, [message.message_id, message.text])
