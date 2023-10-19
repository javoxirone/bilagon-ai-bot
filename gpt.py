import re
import openai
import os


class OpenAIAPI:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API")
        openai.api_key = self.api_key
        self.user_histories = {}  # Dictionary to store conversation histories for each user

    def generate_text(self, telegram_id, message, model="gpt-3.5-turbo", max_tokens=50, temperature=0.7, stop=None):
        try:
            # Prepare the messages by copying the user's chat history
            user_history = self.user_histories.get(telegram_id, [])
            messages = user_history.copy()
            messages.append({"role": "user", "content": message})

            # Generate a response from the model
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                stop=stop
            )

            # Extract the generated response
            generated_text = response.choices[0].message["content"]

            # Append both user and assistant messages to the user's chat history
            user_history.append({"role": "user", "content": message})
            user_history.append({"role": "assistant", "content": generated_text})

            # If needed, modify the response text
            generated_text = re.sub(r'```(.*?)```', r'```monospace\1```', generated_text)

            # Update the user's chat history
            self.user_histories[telegram_id] = user_history

            return generated_text, response
        except Exception as e:
            print(f"Error generating response: {e}")
            return None

    def reset_chat(self, telegram_id):
        if telegram_id in self.user_histories:
            del self.user_histories[telegram_id]
