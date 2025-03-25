![Instagram post - 15](https://github.com/javoxirone/bilagon-ai-bot/assets/70471371/427945b7-6b5e-441d-bf3f-1fdac17b8bf2)

# Bilag'on AI Bot

## Overview

Bilag'on AI Bot is a Telegram bot that leverages AI to provide intelligent and helpful responses to user queries. It supports multiple languages and can process various types of media, including text, images, voice messages, and documents.

## Features

-   **Multi-language Support:** Offers responses and updates in multiple languages (English, Russian, Uzbek).
-   **Media Processing:**
    -   Extracts and interprets text from images using OCR.
    -   Transcribes voice messages into text.
    -   Analyzes content from TXT, DOCX, and PDF documents.
-   **Contextual Conversations:** Maintains conversation history to provide more relevant and coherent responses.
-   **User-Friendly Interface:** Simple and intuitive commands for easy interaction.

## Table of Contents

-   [Setup](#setup)
    -   [Prerequisites](#prerequisites)
    -   [Installation](#installation)
    -   [Configuration](#configuration)
    -   [Environment Variables](#environment-variables)
-   [Running the Project](#running-the-project)
-   [Project Structure](#project-structure)
-   [Contributing](#contributing)
-   [License](#license)
-   [Contact](#contact)

## Setup

Follow these instructions to set up and run the Bilag'on AI Bot.

### Prerequisites

Before you begin, ensure you have the following installed:

-   **Python 3.7+**: Download from [Python Official Website](https://www.python.org/downloads/).
-   **pip**: Python package installer (usually included with Python installation).
-   **Redis**: Required for Celery task management. Install from [Redis Official Website](https://redis.io/download).
-   **Tesseract OCR**: Required for image processing. Follow the installation guide from [Tesseract OCR Documentation](https://tesseract-ocr.github.io/tessdoc/Installation.html).

### Installation

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/javoxirone/bilagon-ai-bot.git
    cd bilagon-ai-bot
    ```

2.  **Create a Virtual Environment:**

    ```bash
    python -m venv venv
    ```

3.  **Activate the Virtual Environment:**

    -   On Windows:

        ```bash
        venv\Scripts\activate
        ```

    -   On macOS and Linux:

        ```bash
        source venv/bin/activate
        ```

4.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    If you don't have a `requirements.txt` file, generate it using:

    ```bash
    pip freeze > requirements.txt
    ```

### Configuration

1.  **Database Setup:**
    -   Ensure PostgreSQL is installed and running.
    -   Create a database for the bot:

        ```sql
        CREATE DATABASE database_name;
        CREATE USER username WITH PASSWORD 'password';
        GRANT ALL PRIVILEGES ON DATABASE database_name TO username;
        ```

    -   Update the `.env` file with your database credentials.

2.  **API Keys:**
    -   Obtain a Telegram Bot token from BotFather on Telegram.
    -   Obtain an OpenAI API key from [OpenAI](https://platform.openai.com/).
    -   Update the `.env` file with these API keys.

### Environment Variables

Create a `.env` file in the root directory of the project and add the following environment variables:

```
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
OPENAI_BASE_URL=YOUR_OPENAI_BASE_URL (Optional: If you have a custom base URL)

DB_NAME=your_database_name
DB_HOST=localhost
DB_USER=your_database_user
DB_PORT=5432
DB_PASSWORD=your_database_password

WEB_SERVER_HOST=localhost
WEB_SERVER_PORT=8080
WEBHOOK_PATH=/webhook
WEBHOOK_SECRET=your_secret_key
BASE_WEBHOOK_URL=YOUR_BASE_WEBHOOK_URL (e.g., https://yourdomain.com)
```

## Running the Project

1.  **Start the Celery Worker:**

    ```bash
    celery -A tasks worker -l info
    ```

    Ensure Redis is running before starting the Celery worker.

2.  **Run the Main Application:**

    ```bash
    python main.py
    ```

    This command starts the Telegram bot using the configurations provided in the `.env` file.

## Project Structure

```
bilagon-ai-bot/
├── api/                      # Interfaces with external APIs (OpenAI)
│   ├── openai/               # OpenAI API integration
│   │   ├── base.py           # Base class for OpenAI API interactions
│   │   ├── processors/       # Modules for processing different types of data
│   │   │   ├── audio.py      # Audio processing module
│   │   │   ├── image.py      # Image processing module
│   │   │   └── text.py       # Text processing module
│   │   └── __init__.py
│   └── __init__.py
├── bot/                      # Telegram bot configurations
│   ├── bot.py                # Router configuration for bot handlers
│   ├── handlers/             # Defines bot handlers for different commands and messages
│   │   ├── admin/            # Handlers for admin-related commands
│   │   ├── user/             # Handlers for user-related commands
│   │   │   ├── callback_handlers.py  # Handles callback queries
│   │   │   ├── command_handlers.py   # Handles command messages
│   │   │   ├── document_handler.py   # Handles document messages
│   │   │   ├── photo_handlers.py      # Handles photo messages
│   │   │   ├── text_handlers.py       # Handles text messages
│   │   │   └── voice_handlers.py      # Handles voice messages
│   │   └── __init__.py
│   ├── middlewares/          # Middleware for request processing
│   │   ├── auth_middleware.py # Authentication middleware
│   │   └── __init__.py
│   └── __init__.py
├── config/                   # Configuration settings
│   ├── constants.py          # Defines constant variables
│   ├── integrations.py       # Integrations with external services
│   └── __init__.py
├── data_types/               # Defines custom data types
│   ├── database.py           # Database data types
│   └── __init__.py
├── database/                 # Database management
│   ├── base.py               # Base class for database interactions
│   ├── repositories/         # Contains database repositories
│   │   ├── conversation.py   # Repository for managing conversations
│   │   └── user.py           # Repository for managing users
│   └── __init__.py
├── decorator/                # Custom decorators
│   ├── status_message_manager.py  # Manages status messages
│   └── __init__.py
├── exceptions/               # Defines custom exceptions
│   ├── api.py                # API exceptions
│   ├── database.py           # Database exceptions
│   └── service.py            # Service exceptions
├── keyboards/                # Defines bot keyboards
│   ├── inline_keyboards.py   # Defines inline keyboards
│   └── keyboards.py          # Defines other keyboards
├── media/                    # Directory for storing media files
├── parser/                   # Document parser
│   ├── document.py           # Parses document content
│   └── __init__.py
├── services/                 # Business logic services
│   ├── api/                  # API-related services
│   │   └── openai_api_services.py  # Services for OpenAI API
│   ├── database/             # Database services
│   │   ├── conversation_database_services.py  # Manages conversation data
│   │   └── user_database_services.py          # Manages user data
│   ├── handler/              # Handler services
│   │   ├── common.py         # Common handler functions
│   │   ├── document_handler_services.py  # Services for document handling
│   │   ├── photo_handler_services.py     # Services for photo handling
│   │   ├── text_handler_services.py      # Services for text handling
│   │   └── voice_handler_services.py     # Services for voice handling
│   └── __init__.py
├── tasks.py                  # Celery tasks
├── templates/                # Message templates
│   ├── message_templates.py  # Defines message templates
│   └── __init__.py
├── tests/                    # Unit tests
│   ├── database/             # Database unit tests
│   │   ├── repositories/     # Tests for database repositories
│   │   │   ├── test_base.py  # Base class for repository tests
│   │   │   ├── test_conversation.py # Tests conversation repo
│   │   │   └── test_user.py        # Tests user repo
│   │   └── test_base.py      # Tests the base.py
│   ├── services/         # Service unit tests
│   │   └── test_user.py  # Tests the user.py
│   └── utils/         # Util unit tests
│   │   └── telegram_api_utils.py  # Tests the telegram_api_utils.py
├── utils/                    # Utility functions
│   ├── api/                  # API utilities
│   │   └── telegram_api_utils.py # Utilities for Telegram API
│   ├── common/               # Common utilities
│   │   ├── datetime_common_utils.py  # Utilities for date and time
│   │   ├── file_common_utils.py      # Utilities for file operations
│   │   └── format_common_utils.py    # Utilities for formatting
│   ├── handler/              # Handler utilities
│   │   └── photo_handler_utils.py    # Utilities for photo handling
│   └── __init__.py
├── announce.py               # Script for sending announcements
├── main.py                   # Main application entry point
├── README.md                 # Project README
├── requirements.txt          # Project dependencies
└── .env                      # Environment variables
```

## Contributing

Contributions to Bilag'on AI Bot are welcome! To contribute:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Implement your changes.
4.  Test your changes thoroughly.
5.  Submit a pull request.

Please follow the coding style and conventions used in the project.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For questions or issues, please open an issue on the [GitHub repository](https://github.com/javoxirone/bilagon-ai-bot). Additionally, you can contact the author of the project through email javoxirone@gmail.com or through [Telegram](https://t.me/javoxirone/).
