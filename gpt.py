import openai
import os
from pprint import pprint


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
        user_history = self.user_histories.get(telegram_id, [])
        user_history.append({"role": "user", "content": user_message})
        user_history.append({"role": "assistant", "content": bot_message})
        self.user_histories[telegram_id] = user_history
        pprint(self.user_histories)

    def reset_chat(self, telegram_id):
        if telegram_id in self.user_histories:
            del self.user_histories[telegram_id]
