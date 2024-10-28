def get_start_command_message(lang: str) -> str:
    message = {
        "uz": "Bilag'on bo'tiga xush kelibsiz. Savolingizni berishingiz mumkin va men javob berishga harakat qilaman!",
        "ru": "Добро пожаловать в чат-бот Bilag'on. Вы можете задавать свои вопросы и я постараюсь на них ответить!",
        "en": "Welcome to Bilag'on chatbot. You can ask your questions and I will try to answer them!",
    }
    return message[lang]


def get_language_command_message(lang: str) -> str:
    message = {
        "uz": "Tilni tanlang:",
        "ru": "Выберите язык:",
        "en": "Choose language:",
    }
    return message[lang]


def get_loading_message(lang: str) -> str:
    message = {
        "uz": "O'ylayapman...",
        "ru": "Я думаю...",
        "en": "I am thinking...",
    }
    return message[lang]


def get_new_chat_message(lang: str) -> str:
    message = {
        "uz": "Botning xotirasidan oxirgi so'rovlaringiz o'chirildi. Endi, boshqa mavzuda savol suhbat boshlashingiz mumkin 😊",
        "ru": "Бот стер память о вашем предыдущем запросе и его ответе. Теперь вы можете выбрать другую тему и начать новый чат 😊",
        "en": "The bot has erased its memory of your previous request and its answer. You can now pick a different topic and start a new chat 😊",
    }
    return message[lang]


def get_examples_command_message(lang: str) -> str:
    message = {
        'uz': '''
• Qiziqarli faktlarni menga ayting, iltimos.
• Python tilini o'rganish uchun qaysi resurslarni tavsiya qilasiz?
• Boshlang'ich dastur olish uchun maslahat berishingiz mumkinmi?
• Musiqa to'plamini o'rganish uchun qaysi darslikni o'qishni tavsiya qilasiz?
• Dunyo bo'ylab sayohat qilish uchun eng qiziqarli joylar qaysilar?
• Sog'liqni saqlash uchun qanday oziq-ovqat tanlash kerak?
• Biznesni boshlash uchun qanday qadamni boshlash kerak?
• Psixologik qanday masalalar haqida yordam bera olishiz mumkin?
• San'atda rivojlanish uchun eng yaxshi usullar nimalardir?
        ''',
        'ru': '''
• Расскажите мне интересные факты, пожалуйста.
• Какие ресурсы вы порекомендуете для изучения языка Python?
• Можете дать совет по получению начального опыта программирования?
• Какую книгу вы посоветуете для изучения музыкальной теории?
• Какие самые интересные места для путешествий по всему миру?
• Как выбирать еду для поддержания здоровья?
• Какие шаги нужно предпринять для начала бизнеса?
• Как вы можете помочь с психологическими вопросами?
• Какие лучшие способы для развития в искусстве?
''',
        'en': '''
• Tell me interesting facts, please.
• What resources would you recommend for learning Python?
• Can you give advice on getting started with programming?
• Which book would you recommend for learning music theory?
• What are the most interesting places to travel around the world?
• How to choose food for maintaining health?
• What steps should be taken to start a business?
• How can you assist with psychological issues?
• What are the best ways to develop in the field of art?
        '''
    }

    return message[lang]


def get_help_command_message(lang: str) -> str:
    message = {
        "uz": "Bilag'on AI Bot dasturimiz GPT til modeli asosida qurilgan bo'lib, foydalanuvchilarga Tez, Oson va Xafvsiz xizmat ko'rsatadi. Quyidagi buyruqlardan foydalanishingiz mumkin: \n"
              "\n"
              "/start - Botni ishga tushirish\n"
              "/help - Bot haqida ma'lumot\n"
              "/settings - Qolgan so'rovlar soni\n"
              "/language - Tilni o'zgartirish\n"
              "/donate - Xayriya bilan qo'llab-quvvatlash\n",

        "ru": "Bilag’on AI Bot работает на языковой модели GPT. Наш Telegram бот обеспечивает <b>быстрое взаимодействие, безопасное общение</b> и <b>удобное использование</b> для своих пользователей. Доступны следующие команды:\n"
              "\n"
              "/start - Запуск бота\n"
              "/help - Информация о боте\n"
              "/settings - Количество оставшихся запросов\n"
              "/language - Поменять язык\n"
              "/examples - Примеры использования\n"
              "/donate - Поддержать благотворительностью\n",
        "en": "Bilag'on AI Bot is powered by GPT language model. This Telegram bot provides <b>Fast Experience, Secure Chatting,</b> and <b>Convenient Use</b> for its users. Following commands are available:\n"
              "\n"
              "/start - Start the bot\n"
              "/help - Information about the bot\n"
              "/settings - Number of remaining requests\n"
              "/language - Change the language\n"
              "/examples - Examples of usage\n"
              "/donate - Supporting by charity\n"
    }
    return message[lang]


def get_token_update_message(lang: str) -> str:
    message = {
        "uz": "Sizga 5ta token qo'shildi",
        "ru": "Вам было добавлено 5 токенов",
        "en": "Your tokens have been updated to 5"
    }
    return message[lang]


def get_no_tokens_message(lang: str) -> str:
    message = {
        'uz': '''
Sizning kunlik soʻrovingiz chegarasi tugadi. Premium foydalanuvchiga yangilash orqali botdan maksimal darajada foydalaning.

Cheksiz oylik tarif atigi 4999 so'm

Server, ma'lumotlar bazasi va API bilan bog'liq xarajatlar to'lanadi. Bundan tashqari, siz botning rivojlanishiga yordam berasiz.
''',
        'ru': '''
Ваш дневной лимит запросов исчерпан. Получите максимальную отдачу от бота, перейдя на премиум-пользователя.

Безлимитный ежемесячный тариф всего за 4999 сум

Затраты, связанные с сервером, базой данных и API, будут оплачены. Кроме того, Вы будете помогать в разработке бота. 
''',
        'en': '''
Your daily request limit has run out. Get the most out of the bot by upgrading to a premium user.

Unlimited monthly tariff for only 4999 UZS

The costs associated with the server, database, and API will be paid for. Furthermore, You will assist in the bot's development.
'''
    }
    return message[lang]


def get_gpt3_payment_successful_message(lang: str) -> str:
    message = {
        'uz': "To'lov muvaffaqiyatli amalga oshirildi ✅",
        'ru': "Оплата успешно завершена ✅",
        'en': "Payment completed successfully ✅"
    }
    return message[lang]


def get_settings_command_message(tariff, requests_num, expiration_date, lang):
    message = {
        'uz': f"Tarif: <b>{tariff}</b>\n"
              f"So'rovlar soni: <b>{requests_num}</b>\n"
              f"Tugash vaqti: <b>{expiration_date}</b>\n"
              f"Botning tili: <b>{lang}</b>\n\n"
              f"<b>Bilag'on AI Bot do'stlaringizga ulashing!</b>",

        'ru': f"Тариф: <b>{tariff}</b>\n"
              f"Количество запросов: <b>{requests_num}</b>\n"
              f"Дата окончания: <b>{expiration_date}</b>\n"
              f"Язык бота: <b>{lang}</b>\n\n"
              f"<b>Поделитесь Bilag'on AI Bot с друзьями!</b>",

        'en': f"Tariff: <b>{tariff}</b>\n"
              f"Number of requests: <b>{requests_num}</b>\n"
              f"Expiration date: <b>{expiration_date}</b>\n"
              f"Bot Language: <b>{lang}</b>\n\n"
              f"<b>Share Bilag'on AI Bot with friends!</b>"
    }
    return message[lang]


def get_premium_requests_num_message(lang: str) -> str:
    message = {
        'uz': "Cheklanmagan",
        'ru': "Неограниченный",
        'en': "Unlimited"
    }
    return message[lang]


def get_donate_command_message(lang: str) -> str:
    message = {
        "uz": "🤖 Bizning chat-botimizni rivojlantirishni qo'llab-quvvatlang!\n"
              "\n"
              "Salom!\n"
              "\n"
              "Sizning chat-bot tajribangizni yaxshilashga yordam bering. Sizning xayriyangiz uni rivojlantirishni ta'minlaydi, siz uchun eng yaxshi tajribani taqdim etadi.\n"
              "\n"
              "🙏 Karta raqami: <code>5614682115259642</code>\n"
              "\n"
              "Rahmat,\n"
              "Bilag'on AI Bot jamoasi\n",

        "ru": "🤖 Поддержите развитие нашего чат-бота!\n"
              "\n"
              "Привет!\n"
              "\n"
              "Помогите нам усовершенствовать ваш опыт чата. Ваше пожертвование обеспечит его развитие, гарантируя лучшего бота для вас.\n"
              "\n"
              "🙏 Карта для пожертвование: <code>5614682115259642</code>\n"
              "\n"
              "Спасибо,\n"
              "Команда Bilag'on AI Bot\n",

        "en": "🤖 Support Our Chatbot's Development!\n"
              "\n"
              "Hello!\n"
              "\n"
              "Help us enhance your chatbot experience. Your donation fuels its growth and improvement, ensuring a better copilot for you.\n"
              "\n"
              "🙏 Card Number: <code>5614682115259642</code>\n"
              "\n"
              "Thank you,\n"
              "Bilag'on AI Bot Team\n"
    }
    return message[lang]


def get_openai_error_message(lang):
    message = {
        'uz': "Keyinroq qayta urinib ko‘ring. Hozirda bizga juda ko'p so'rovlar kelib tushmoqda!",
        'ru': "Попробуйте позже. В настоящее время мы получаем большое количество запросов!",
        'en': "Try again later. We are currently receiving a large number of requests!"
    }
    return message[lang]


def get_bot_error_message(lang):
    message = {
        'uz': "Nimadir noto'g'ri bajarildi! Yangi suhbat boshlashga harakat qiling👇",
        'ru': "Что-то пошло не так! Попробуйте начать новый разговор 👇",
        'en': "Something went wrong! Try starting a new conversation 👇"
    }
    return message[lang]




