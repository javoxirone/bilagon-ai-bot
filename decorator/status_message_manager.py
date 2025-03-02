import functools
from typing import Callable, Any, Dict

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

from services.database.user_database_services import get_user_language
from templates.message_templates import get_processing_message


class StatusMessageManager:
    """Manages status messages for long-running operations with duplicate prevention."""

    def __init__(self, bot):
        self.bot = bot
        self._status_cache = {}  # Cache to track current status message text

    async def with_status_updates(self,
                                  message: Message,
                                  status_steps: Dict[str, str],
                                  func: Callable,
                                  *args, **kwargs) -> Any:
        """
        Execute a function with status updates at each defined step.
        """
        telegram_id = message.from_user.id
        user_language = get_user_language(telegram_id)
        # Send initial status message
        initial_status = list(status_steps.values())[0] if status_steps else get_processing_message(user_language)
        status_message = await message.reply(initial_status)
        status_message_id = status_message.message_id

        # Initialize cache entry for this message
        cache_key = f"{telegram_id}:{status_message_id}"
        self._status_cache[cache_key] = initial_status

        # Create a context object to pass to the function
        status_context = {
            "telegram_id": telegram_id,
            "status_message_id": status_message_id,
            "current_step": None,
            "update_status": self._create_status_updater(telegram_id, status_message_id, status_steps)
        }

        try:
            # Execute the function with the context
            return await func(*args, **kwargs, status_context=status_context)
        except Exception as e:
            # Handle any exceptions
            error_message = f"Error during processing: {str(e)}"
            await self._safe_update_message(telegram_id, status_message_id, error_message)
            raise
        finally:
            # Clean up cache entry
            if cache_key in self._status_cache:
                del self._status_cache[cache_key]

    def _create_status_updater(self, telegram_id: int, status_message_id: int, status_steps=None):
        """Creates a status update function for a specific message."""

        if status_steps is None:
            status_steps = {}

        async def update_status(step_name: str):
            # Convert step name to actual message text
            if step_name in status_steps:
                text = status_steps[step_name]
                await self._safe_update_message(telegram_id, status_message_id, text)
            else:
                # Handle unknown step names
                await self._safe_update_message(telegram_id, status_message_id, step_name)

        return update_status

    async def _safe_update_message(self, chat_id: int, message_id: int, text: str) -> bool:
        """
        Update a message only if the text has changed to avoid the 'message is not modified' error.

        Returns:
            bool: True if message was updated, False if update was skipped
        """
        cache_key = f"{chat_id}:{message_id}"

        # Skip update if text hasn't changed
        if cache_key in self._status_cache and self._status_cache[cache_key] == text:
            return False

        try:
            await self.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text
            )
            # Update cache
            self._status_cache[cache_key] = text
            return True
        except TelegramBadRequest as e:
            # Handle the specific error
            if "message is not modified" in str(e):
                # This is expected sometimes, just ignore it
                return False
            else:
                # For other BadRequest errors, re-raise
                raise

    def status_update_decorator(self, status_steps=None):
        """
        Decorator that wraps a function with status updates.
        """

        if status_steps is None:
            status_steps = {}

        def decorator(func):
            @functools.wraps(func)
            async def wrapper(message, *args, **kwargs):
                return await self.with_status_updates(message, status_steps, func, message, *args, **kwargs)

            return wrapper

        return decorator