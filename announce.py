import asyncio
from bot.bot import bot
from database.user import User


def get_announcement_message(lang, first_name):
    message = {
        'uz': f"Salom, {first_name} 👋\n\nBotning yangi xususiyatlarini kashf eting:\n- Chat-bot gpt-4o-mini modeliga yangilandi\n- Ovozni tanib olish\n- Rasmdan matnni tanib olish\n- Matnli fayllarni tanib olish (DOCX, TXT, PDF)\n- Xatolar tuzatildi.\n\n<strong>To'liq bepul va ochiq manba Bilagon AI Bot'dan foydalanishdan zavqlaning!</strong>",

        'ru': f"Здравствуйте, {first_name} 👋\n\nИзучите новые возможности бота:\n- Чат-бот обновлен до модели gpt-4o-mini\n- Распознавание голосовых сообщений\n- Распознавание текста с изображения\n- Распознавание текстовых файлов (DOCX, TXT, PDF)\n- Исправлены ошибки.\n\n<strong>Наслаждайтесь использованием полностью бесплатного и открытого Bilagon AI Bot!</strong>",

        'en': f"Hello, {first_name} 👋\n\nExplore new features of the bot:\n- Chat-bot was upgraded to gpt-4o-mini model\n- Voice message recognition\n- Text recognition from the image\n- Text file recognition (DOCX, TXT, PDF)\n- Fixed bugs. \n\n<strong>Enjoy using fully free and open-source Bilagon AI Bot!</strong>"
    }

    return message.get(lang, message['en'])


async def handle_announcement():
    user = User()
    users = user.get_all_users()
    user.close()

    tasks = [
        bot.send_message(user["telegram_id"], get_announcement_message(user["language"], user["first_name"]),
                         parse_mode="HTML")
        for user in users
    ]

    await asyncio.gather(*tasks)


async def main():
    async with bot.session:
        await handle_announcement()


if __name__ == '__main__':
    asyncio.run(main())
