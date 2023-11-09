# BilagonAIBot

This project is a simple example of a Telegram bot developed using the aiogram library in Python. The bot can be used as a starting point for implementing more complex Telegram bots.

## Installation

1. Clone the repository to your local machine:

$ git clone https://github.com/username/aiogram-python-bot.git


2. Change into the project directory:

$ cd aiogram-python-bot


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

Once the bot is up and running, you can interact with it through the Telegram app. Search for your bot by its username, and send messages or commands to test its functionality.

The bot currently supports the following commands:

- /start: Displays a welcome message and instructions on how to use the bot.
- /help: Displays a help message with a brief explanation of each command.
- /echo <message>: The bot echoes the provided message.

## Contributing

Contributions to this project are welcome. Feel free to open issues or submit pull requests with any improvements or new features you would like to add.

Before contributing, please make sure to read the Contributing Guidelines (http://contributing.md/).

## License

This project is licensed under the MIT License.
