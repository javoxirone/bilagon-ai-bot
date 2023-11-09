# Bilag'on AI Bot Powered by GPT

This project is a Telegram bot developed using the aiogram library in Python. The bot utilizes the power of GPT (Generative Pre-trained Transformer) to generate intelligent and contextually relevant responses. It can be used as a starting point for building advanced AI-powered Telegram bots.

## Installation

1. Clone the repository to your local machine:

$ git clone https://github.com/username/bilagon-ai-bot.git


2. Change into the project directory:

$ cd bilagon-ai-bot


3. Create and activate a new virtual environment:

$ python3 -m venv env
$ source env/bin/activate


4. Install the required dependencies:

$ pip install -r requirements.txt


5. Set up your Telegram bot token:

   - Create a new bot on Telegram by following the instructions provided by the BotFather (https://core.telegram.org/bots#botfather).
   - Copy the bot token obtained from the BotFather.

   - Open the config.py file and replace <YOUR_BOT_TOKEN> with your actual bot token.

6. Run the bot:

$ python bot.py


## Usage

Once the bot is up and running, you can interact with it through the Telegram app. Search for your bot by its username, and send messages or commands to initiate AI-generated responses.

The bot understands a variety of commands and responds accordingly. Some of the supported commands are:

- /start: Displays a welcome message and instructions on how to use the bot.
- /help: Provides assistance on using the bot and explains available commands.
- /ask <question>: Sends the provided question to the AI model for generating an intelligent response.

Feel free to experiment and ask the bot different questions to explore its capabilities.

## Contributing

Contributions to this project are welcome. If you have any improvements or new features to add, please open an issue or submit a pull request.

Before contributing, please read the Contributing Guidelines (http://contributing.md/).

## License

This project is licensed under the MIT License.
