import asyncio
from bot.bot import bot
from database.user import User


def get_announcement_message(lang, first_name):
    message = {
        'uz': f"Salom, {first_name} 👋\n\nBotning yangi xususiyatlarini sinab ko'ring:\n- Bundan buyon Grok by xAI bot uchun asosiy model sifatida foydalanilmoqda.\n",

        'ru': f"Здравствуйте, {first_name} 👋\n\nИзучите новые возможности бота:\n- Отныне Grok от xAI используется в качестве основной модели бота.\n",

        'en': f"Hello, {first_name} 👋\n\nExplore new features of the bot:\n- From now on, Grok by xAI is being used as a primary model for the bot.\n"
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
