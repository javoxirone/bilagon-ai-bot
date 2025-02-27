import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from bot.bot import admin_router, user_router
from bot.middlewares.auth_middleware import auth_middleware
# from bot.middlewares.auth_middleware import auth_middleware
from config.constants import (
    BASE_WEBHOOK_URL,
    WEBHOOK_PATH,
    WEBHOOK_SECRET,
    BOT_TOKEN, WEB_SERVER_HOST, WEB_SERVER_PORT,
)

# Set up logging for better debugging
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG for more detailed logs
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


async def on_startup(bot: Bot) -> None:
    """
    Perform startup actions like setting the webhook.
    """
    try:
        webhook_url = f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}"
        logger.info("Setting up webhook at %s", webhook_url)
        await bot.set_webhook(webhook_url, secret_token=WEBHOOK_SECRET)
        logger.info("Webhook set successfully.")
    except Exception as e:
        logger.error("Error during webhook setup: %s", str(e), exc_info=True)
        raise


def main() -> None:
    """
    Main entry point for the application.
    """
    logger.info("Starting bot application...")

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(user_router)
    dp.include_router(admin_router)
    dp.update.outer_middleware(auth_middleware)

    # Create Aiohttp web application
    app = web.Application()

    try:
        # Initialize webhook request handler
        webhook_requests_handler = SimpleRequestHandler(
            dispatcher=dp,
            bot=bot,
            secret_token=WEBHOOK_SECRET,
        )
        logger.debug("Webhook request handler initialized.")

        # Register webhook path
        webhook_requests_handler.register(app, path=WEBHOOK_PATH)
        logger.debug("Webhook path registered at %s", WEBHOOK_PATH)

        # Set up the application with dispatcher and bot
        setup_application(app, dp, bot=bot)
        logger.debug("Application setup completed.")

        # Start the web server
        logger.info("Starting web server at %s:%s", WEB_SERVER_HOST, WEB_SERVER_PORT)
        web.run_app(app, host=WEB_SERVER_HOST, port=int(WEB_SERVER_PORT))
    except Exception as e:
        logger.error("An error occurred in the main function: %s", str(e), exc_info=True)


if __name__ == "__main__":
    try:
        main()

    except Exception as e:
        logger.critical("Unhandled exception: %s", str(e), exc_info=True)
        sys.exit(1)
