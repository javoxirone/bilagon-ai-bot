# Bilag'on AI Bot Powered by GPT

This project is a Telegram bot developed using the aiogram library in Python. The bot utilizes the power of GPT (Generative Pre-trained Transformer) to generate intelligent and contextually relevant responses. It can be used as a starting point for building advanced AI-powered Telegram bots.

## Installation

1. Clone the repository to your local machine:
```cmd
git clone https://github.com/username/bilagon-ai-bot.git
```

2. Change into the project directory:
```cmd
cd bilagon-ai-bot
```

3. Create and activate a new virtual environment:
For Linux users:
```cmd
python3 -m venv env
source env/bin/activate
```

For Windows users:
```cmd
python -m venv env
cd env/Scripts/activate
```

4. Install the required dependencies:
```cmd
pip install -r requirements.txt
```

5. Set up your Telegram bot token:

   - Create .env file
   - Create a new bot on Telegram by following the instructions provided by the BotFather (https://core.telegram.org/bots#botfather).
   - Copy and paste the following fields to .env file, and fill them out:
      ```.env
      OPENAI_API = '<YOUR_OPEN_AI_API_KEY>'
      BOT_TOKEN = '<YOUR_BOT_TOKEN>'
      DB_NAME = '<YOUR_DB_NAME>'
      DB_HOST = '<YOUR_DB_HOST>'
      DB_USER = '<YOUR_DB_USER>'
      DB_PORT = '5432'
      DB_PASSWORD = '<YOUR_DB_PASSWORD>'
      ```

6. Run the bot:
For Linux users:
```cmd
python3 main.py
```

For Windows users:
```cmd
python main.py
```

## Usage

Once the bot is up and running, you can interact with it through the Telegram app. Search for your bot by its username, and send messages or commands to initiate AI-generated responses.

The bot understands a variety of commands and responds accordingly. Some of the supported commands are:
```
/start - Start the bot
/help - Information about the bot
/settings - Number of remaining requests
/language - Change the language
/examples - Examples of usage
/donate - Supporting by charity
```
Feel free to experiment and ask the bot different questions to explore its capabilities.

## Contributing

Contributions to this project are welcome. If you have any improvements or new features to add, please open an issue or submit a pull request.
