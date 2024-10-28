import os
from pprint import pprint
from database.conversation import Conversation
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class OpenAIAPI:
    def __init__(self, api_key=None):
        self.api_key: str = api_key or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
        self.user_histories: dict = {}

    def generate_response(
        self,
        model: str = "gpt-4o-mini",
        max_tokens: int = 50,
        messages: list | None = None,
        temperature: float = 0.7,
        stop=None,
    ) -> any:
        """
        This method sends request to OpenAI model and gets response from the API.

        :param model: (optional) the name of the OpenAI model in string format.
        :param max_tokens: (optional) the maximum number of tokens models should generate.
        :param messages: (optional) request of the user in List format.
        :param temperature: (optional) how should model answer more general or exact.
        :param stop: (optional) when the models should stop genearting response.
        """
        try:
            response = self.client.chat.completions.create(
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

    def update_user_histories(
        self, telegram_id: int, user_message: str, bot_message: str
    ) -> None:
        """
        This method gets three arguments telegram_id, user_message, and bot_message and saves them in db, table conversations.

        :param telegram_id: Unique id of the telegram user.
        :param user_message: Message of the user (request from the user in string format).
        :param bot_message: Message of the assistant (full response from the GPT model in string format).
        """
        db: object = Conversation()
        db.add_conversation(telegram_id, "user", user_message)
        db.add_conversation(telegram_id, "assistant", bot_message)
        db.close()

    def reset_chat(self, telegram_id) -> None:
        """
        This method gets telegram_id of the user and clears out all conversations related to that user.

        :param telegram_id: Unique ID of the telegram user.
        """
        db: object = Conversation()
        db.reset_conversations(telegram_id)
        db.close()
