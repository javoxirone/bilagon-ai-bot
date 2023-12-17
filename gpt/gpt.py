import openai
import os
from pprint import pprint
from database.base import Database
from database.conversation import Conversation


class OpenAIAPI:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API")
        openai.api_key = self.api_key
        self.user_histories = {}

    def generate_response(self, model="gpt-3.5-turbo", max_tokens=50, messages: list | None = None, temperature=0.7,
                          stop=None):
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
                stop=stop,
            )

            return response
        except Exception as e:
            pprint(f"Error generating response: {e}")
            return None

    def update_user_histories(self, telegram_id, user_message, bot_message):
        db = Conversation()
        db.add_conversation(telegram_id, "user", user_message)
        db.add_conversation(telegram_id, "assistant", bot_message)
        db.close()

    def reset_chat(self, telegram_id):
        db = Conversation()
        db.reset_conversations(telegram_id)
        db.close()
