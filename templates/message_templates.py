from config.constants import MODELS


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
        "uz": "Botning xotirasidan oxirgi so'rovlaringiz o'chirildi. Endi, boshqa mavzuda savol suhbat boshlashingiz mumkin!",
        "ru": "Бот стер память о вашем предыдущем запросе и его ответе. Теперь вы можете выбрать другую тему и начать новый чат!",
        "en": "The bot has erased its memory of your previous request and its answer. You can now pick a different topic and start a new chat!",
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


def get_settings_command_message(telegram_id: int, lang: str, saved_conversation_mode: bool, model_name: str) -> str:
    incognito_mode_message = {
        "uz": ("Yoqilgan 🫥", "O'chirilgan"),
        "ru": ("Включен 🫥", "Выключен"),
        "en": ("Active 🫥", "Inactive")
    }
    incognito_mode = incognito_mode_message[lang][1] if saved_conversation_mode else incognito_mode_message[lang][0]
    message = {
        'uz': f"Telegram ID: <b>{telegram_id}</b>\n"
              f"Botning tili: <b>{lang}</b>\n"
              f"Inkognito rejimi: <b>{incognito_mode}</b>\n"
              f"Suniy Idrok modeli: <b>{model_name}</b>\n\n"
              f"<b>\"Bilag'on\"ni  do'stlaringiz bilan ulashing!</b>",

        'ru': f"Telegram ID: <b>{telegram_id}</b>\n"
              f"Язык бота: <b>{lang}</b>\n"
              f"Режим инкогнито: <b>{incognito_mode}</b>\n"
              f"Модель ИИ: <b>{model_name}</b>\n\n"
              f"<b>Поделитесь Bilag'on с друзьями!</b>",

        'en': f"Telegram ID: <b>{telegram_id}</b>\n"
              f"Bot Language: <b>{lang}</b>\n"
              f"Incognito mode: <b>{incognito_mode}</b>\n"
              f"AI model: <b>{model_name}</b>\n\n"
              f"<b>Share Bilag'on with friends!</b>"
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


def get_chat_mode_message(lang):
    message = {
        'uz': "Bot ixtisoslashishini xohlagan suhbat rejimini tanlang.",
        'ru': "Выберите режим чата, в котором бот будет специализироваться.",
        'en': "Select the chat mode you want the bot to specialize in."
    }
    return message[lang]


def get_processing_voice_message(lang):
    message = {
        'uz': 'Ovozli xabaringiz qayta ishlanmoqda...',
        'ru': 'Обработка вашего голосового сообщения...',
        'en': 'Processing your voice message...',
    }
    return message[lang]


def get_downloading_voice_message(lang):
    message = {
        'uz': 'Ovozli xabar yuklab olinmoqda...',
        'ru': 'Загрузка голосового сообщения...',
        'en': 'Downloading the voice message...',
    }
    return message[lang]


def get_transcribing_voice_message(lang):
    message = {
        'uz': 'Ovozli xabaringiz transkripsiya qilinmoqda...',
        'ru': 'Транскрибация вашего голосового сообщения...',
        'en': 'Transcribing your voice message...',
    }
    return message[lang]


def get_generating_response_message(lang):
    message = {
        'uz': 'Javob yaratilmoqda...',
        'ru': 'Формирование ответа...',
        'en': 'Generating the response...',
    }
    return message[lang]


def get_processing_photo_message(lang):
    message = {
        'uz': 'Surat qayta ishlanmoqda...',
        'ru': 'Обработка фото...',
        'en': 'Processing your photo...',
    }
    return message[lang]


def get_downloading_photo_message(lang):
    message = {
        'uz': 'Surat yuklab olinmoqda...',
        'ru': 'Загружаю фото...',
        'en': 'Downloading the photo...',
    }
    return message[lang]


def get_extracting_text_from_photo_message(lang):
    message = {
        'uz': 'Suratdan matn olinmoqda...',
        'ru': 'Извлечение текста из фотографии...',
        'en': 'Extracting the text from the photo...',
    }
    return message[lang]


def get_final_request_message(lang):
    message = {
        'uz': 'Yakuniy so‘rov tayyorlanmoqda...',
        'ru': 'Подготовка окончательного запроса...',
        'en': 'Preparing the final request...',
    }
    return message[lang]


def get_processing_document_message(lang):
    message = {
        'uz': 'Hujjatingiz qayta ishlanmoqda...',
        'ru': 'Обработка вашего документа...',
        'en': 'Processing your document...',
    }
    return message[lang]


def get_downloading_document_message(lang):
    message = {
        'uz': 'Hujjat yuklab olinmoqda...',
        'ru': 'Загрузка документа...',
        'en': 'Downloading the document...',
    }
    return message[lang]


def get_parsing_content_message(lang):
    message = {
        'uz': 'Kontent tahlil qilinmoqda...',
        'ru': 'Анализ содержимого...',
        'en': 'Parsing the content...',
    }
    return message[lang]


def get_processing_text_message(lang):
    message = {
        'uz': 'Matnli xabaringiz qayta ishlanmoqda...',
        'ru': 'Обработка вашего текстового сообщения...',
        'en': 'Processing your text message...',
    }
    return message[lang]


def get_processing_message(lang):
    message = {
        'uz': 'Qayta ishlanmoqda...',
        'ru': 'Обработка...',
        'en': 'Processing...',
    }
    return message[lang]


def get_suggestions_message(lang):
    message = {
        'uz': 'Suhbatni davom ettirish uchun taklif qilingan savollardan birini tanlashingiz mumkin.',
        'ru': 'Вы можете выбрать один из предложенных вопросов, чтобы продолжить разговор.',
        'en': 'You can choose one of the suggested questions to continue the conversation.',
    }
    return message[lang]


def get_no_suggestions_message(lang):
    message = {
        'uz': 'Hozircha hech qanday taklif yo\'q.',
        'ru': 'На данный момент предложений нет.',
        'en': 'There is no suggestions for now.',
    }
    return message[lang]


def get_contribute_message(lang):
    message = {
        'uz': (
            "Ochiq manba kodiga hissa qo'shish - bu dasturlash ko'nikmalaringizni oshirish va hamjamiyatga yordam berish uchun ajoyib imkoniyat. "
            "Bilag'on loyihasiga qo'shiling va katta narsaning bir qismi bo'ling! Siz xatolarni tuzatish, yangi funksiyalar qo'shish yoki hujjatlarni yaxshilash orqali hissa qo'shishingiz mumkin.\n\n"
            "Qo'shimcha ma'lumot va boshlash uchun bizning repozitoriyamizga tashrif buyuring: [Bilag'on on GitHub](https://github.com/javoxirone/bilagon-ai-bot). "
            "Sizning g'oyalaringiz va sa'y-harakatlaringiz biz uchun muhim!"
        ),
        'ru': (
            "Внесение вклада в открытый исходный код — это отличный способ улучшить свои навыки программирования и помочь сообществу. "
            "Присоединяйтесь к проекту Bilag'on и станьте частью чего-то большего! Вы можете внести свой вклад, исправляя ошибки, добавляя новые функции или улучшая документацию.\n\n"
            "Для получения дополнительной информации и начала работы, посетите наш репозиторий: [Bilag'on на GitHub](https://github.com/javoxirone/bilagon-ai-bot). "
            "Ваши идеи и усилия важны для нас!"
        ),
        'en': (
            "Contributing to open-source is a great way to enhance your programming skills and help the community. "
            "Join the Bilag'on project and be part of something bigger! You can contribute by fixing bugs, adding new features, or improving documentation.\n\n"
            "For more information and to get started, visit our repository: [Bilag'on on GitHub](https://github.com/javoxirone/bilagon-ai-bot). "
            "Your ideas and efforts matter to us!"
        ),
    }
    return message[lang]


def get_activated_context_message(lang):
    message = {
        'uz': 'Kontekst hozirda faollashtirildi. Endi yordamchi suhbat tarixini saqlaydi va yangi suhbat boshlangunga qadar umumiy suhbat kontekstni tushunadi.',
        'ru': 'Контекст теперь активирован. С этого момента помощник будет сохранять историю беседы и понимать общий контекст до начала нового чата.',
        'en': 'The context is now activated. From this moment on, the assistant will retain the conversation history and comprehend the overall context until a new chat is initiated.',
    }
    return message[lang]


def get_models_message(lang):
    message = {
        'uz': 'Quyida t\'o\'gri keladigan suniy idrok modelini tanlang:',
        'ru': 'Выберите одну из подходящих моделей ИИ ниже:',
        'en': 'Please select one of the appropriate AI models below:'
    }
    return message[lang]


def get_models(lang: str):
    translations = {
        'en': {
            'Fast, smart, general use': 'Fast, smart, general use',
            'Balanced, chat, coding, writing': 'Balanced, chat, coding, writing',
            'Ultra-fast, real-time responses': 'Ultra-fast, real-time responses',
            'Fast, automation, quick replies': 'Fast, automation, quick replies',
            'Smarter, reasoning, complex tasks': 'Smarter, reasoning, complex tasks',
            'Coming soon': 'Coming soon'
        },
        'uz': {
            'Fast, smart, general use': 'Tez, aqlli, umumiy foydalanish',
            'Balanced, chat, coding, writing': 'Muvozanatli, chat, dasturlash, yozish',
            'Ultra-fast, real-time responses': 'Juda tez, real vaqt javoblari',
            'Fast, automation, quick replies': 'Tez, avtomatlashtirish, tezkor javoblar',
            'Smarter, reasoning, complex tasks': 'Aqlliroq, tahlil, murakkab vazifalar',
            'Coming soon': 'Tez orada'
        },
        'ru': {
            'Fast, smart, general use': 'Быстрый, умный, универсальный',
            'Balanced, chat, coding, writing': 'Сбалансированный, чат, кодинг, написание',
            'Ultra-fast, real-time responses': 'Сверхбыстрые ответы в реальном времени',
            'Fast, automation, quick replies': 'Быстро, автоматизация, быстрые ответы',
            'Smarter, reasoning, complex tasks': 'Умнее, анализ, сложные задачи',
            'Coming soon': 'Скоро'
        }
    }

    if lang not in translations:
        lang = 'en'  # Default to English if the language is not supported

    return {model: translations[lang][desc] for model, desc in MODELS.items()}
