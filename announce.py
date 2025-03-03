import asyncio
import logging
from aiogram import Bot, Dispatcher
import asyncpg
import os

from aiogram.enums import ParseMode
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot token from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Database connection parameters
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "database")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASSWORD", "postgres")

# Announcement messages for different languages
ANNOUNCEMENTS = {
    "en": """📢 *Bilag'on 1.1.0 Update – Smarter, Faster, Better!*

🚀 *Big News!*
Bilag'on just got a major upgrade! With version 1.1.0, your favorite AI-powered assistant is now more efficient, smarter, and packed with new features to make your experience even better.

🎯 *What's New?*

🏗 *Smoother Performance:*
- The bot now responds faster and handles requests more efficiently.
- Improved system stability for a seamless experience.

🤖 *Smarter AI Features:*
- OpenAI integration is now optimized for better accuracy.
- Text generation is more natural and reliable.

🖼 *New Media Capabilities:*
- Convert images to text effortlessly.
- Use voice-to-text for quick and easy communication.

🌍 *Enhanced User Experience:*
- Get updates and messages in multiple languages.
- Enjoy smart suggestions to make your conversations even more engaging.

🛠 *Bug Fixes & Optimizations:*
- We've cleaned up old code and removed unnecessary dependencies.
- Various issues have been fixed to improve overall stability.

🎉 *Ready to Try?*
Bilag'on 1.1.0 is here to make your experience smoother, faster, and more intuitive. Thank you for being a part of the journey—enjoy the new features! 🚀""",

    "ru": """📢 *Обновление Bilag'on 1.1.0 – Умнее, Быстрее, Лучше!*

🚀 *Большие новости!*
Bilag'on получил серьезное обновление! В версии 1.1.0 ваш любимый AI-ассистент стал еще эффективнее, умнее и удобнее в использовании.

🎯 *Что нового?*

🏗 *Более плавная работа:*
- Бот теперь отвечает быстрее и работает стабильнее.
- Улучшена стабильность системы для комфортного использования.

🤖 *Умные AI-функции:*
- Интеграция с OpenAI стала еще точнее.
- Генерация текста теперь более естественная и надежная.

🖼 *Новые мультимедийные возможности:*
- Легко конвертируйте изображения в текст.
- Используйте голосовой ввод для удобного общения.

🌍 *Улучшенный пользовательский опыт:*
- Обновления и сообщения теперь доступны на нескольких языках.
- Умные подсказки помогут сделать ваши беседы еще удобнее.

🛠 *Исправления ошибок и оптимизация:*
- Удален устаревший код и ненужные зависимости.
- Исправлены различные ошибки для повышения стабильности.

🎉 *Попробуйте прямо сейчас!*
Bilag'on 1.1.0 стал еще удобнее, быстрее и умнее. Спасибо, что вы с нами! Наслаждайтесь новыми функциями! 🚀""",

    "uz": """📢 *Bilag'on 1.1.0 Yangilanishi – Aqlliroq, Tezroq, Yaxshiroq!*

🚀 *Katta yangiliklar!*
Bilag'on katta yangilanish oldi! 1.1.0 versiyasi bilan sevimli AI-yordamchingiz endi yanada samarali, aqlli va foydalanuvchilarga qulay bo'ldi.

🎯 *Nimalar yangilandi?*

🏗 *Tezroq va barqaror ishlash:*
- Bot endi tezroq javob beradi va yanada samarali ishlaydi.
- Tizim barqarorligi yaxshilandi.

🤖 *Aqlli AI imkoniyatlari:*
- OpenAI integratsiyasi yanada aniqroq ishlaydi.
- Matn generatsiyasi yanada tabiiy va ishonchli bo'ldi.

🖼 *Yangi media imkoniyatlari:*
- Rasmlarni osongina matnga aylantiring.
- Tez va qulay muloqot uchun ovozni matnga aylantirish funksiyasi qo'shildi.

🌍 *Foydalanuvchi tajribasini yaxshilash:*
- Yangiliklar va xabarlar endi bir nechta tillarda mavjud.
- Aqlli tavsiyalar muloqotni yanada qiziqarli qiladi.

🛠 *Xatolar tuzatildi va tizim optimallashtirildi:*
- Eskirgan kod va keraksiz kutubxonalar olib tashlandi.
- Barqarorlikni oshirish uchun turli xatolar tuzatildi.

🎉 *Sinab ko'rishga tayyormisiz?*
Bilag'on 1.1.0 endi yanada tezkor, aqlli va qulay. Biz bilan bo'lganingiz uchun rahmat! Yangi imkoniyatlardan bahramand bo'ling! 🚀"""
}

# Default language if user's preference is not available
DEFAULT_LANGUAGE = "en"


async def send_announcements():
    # Create bot instance
    bot = Bot(token=BOT_TOKEN)

    try:
        # Connect to database
        logger.info("Connecting to the database...")
        conn = await asyncpg.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )

        logger.info("Connected to database. Fetching users...")

        # Fetch all users with telegram_id and language
        users = await conn.fetch("SELECT telegram_id, language FROM users")

        logger.info(f"Found {len(users)} users to notify")

        # Send announcements to each user
        success_count = 0
        failed_count = 0

        for user in users:
            telegram_id = user['telegram_id']
            language = user['language'] if user['language'] in ANNOUNCEMENTS else DEFAULT_LANGUAGE

            try:
                # Get the appropriate announcement for the user's language
                announcement = ANNOUNCEMENTS[language]

                # Send the message
                await bot.send_message(
                    chat_id=telegram_id,
                    text=announcement,
                    parse_mode=ParseMode.MARKDOWN
                )

                success_count += 1

                # Add delay to avoid hitting rate limits
                await asyncio.sleep(0.05)

                # Log progress for every 100 users
                if success_count % 100 == 0:
                    logger.info(f"Progress: {success_count}/{len(users)} messages sent")

            except Exception as e:
                logger.error(f"Failed to send message to user {telegram_id}: {e}")
                failed_count += 1

        logger.info(f"Announcement sending completed. Successful: {success_count}, Failed: {failed_count}")

    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        # Close database connection
        if 'conn' in locals():
            await conn.close()
            logger.info("Database connection closed")

        # Close bot session
        await bot.session.close()
        logger.info("Bot session closed")


if __name__ == "__main__":
    logger.info("Starting announcement sender...")

    # Run the announcement sender
    asyncio.run(send_announcements())

    logger.info("Process completed")