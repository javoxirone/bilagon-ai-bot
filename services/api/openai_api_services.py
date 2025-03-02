import json
from typing import BinaryIO

from config.integrations import text_processor, audio_processor
from services.database.conversation_database_services import get_conversation_list
from services.database.user_database_services import get_user_language


def get_text_response(context: list, user_language: str = "en"):
    stream = text_processor.generate_text_response(
        messages=[{
            "role": "developer",
            "content": (
                f"You are **Bilag'on**, an intelligent and highly capable assistant. "
                f"Your primary goal is to provide clear, concise, and insightful responses in {user_language} language. "
                f"You can process and analyze various types of media, including:\n\n"
                f"- **Images**: Extract and interpret text accurately.\n"
                f"- **Voice Messages**: Transcribe audio to text and respond meaningfully.\n"
                f"- **Documents (TXT, DOCX, PDF)**: Retrieve and analyze document content.\n"
                f"- **Text Messages**: Understand and respond to user queries effectively.\n\n"
                f"Always prioritize accuracy, clarity, and usefulness in your responses."
            )
        }] + context,
        stream=True,
        max_tokens=2000
    )
    return stream


def get_text_response_in_incognito_mode(user_message: str, user_language: str = "en"):
    stream = get_text_response([{"role": "user", "content": user_message}], user_language)
    for chunk in stream:
        if chunk.choices[0].delta.content is not None and chunk.choices[0].delta.content != "":
            yield chunk.choices[0].delta.content


def get_text_response_with_context(conversation_list: list, user_language: str = "en"):
    stream = get_text_response(conversation_list, user_language)
    for chunk in stream:
        if chunk.choices[0].delta.content is not None and chunk.choices[0].delta.content != "":
            yield chunk.choices[0].delta.content


def get_transcription_of_audio(audio_file: BinaryIO) -> str:
    transcription = audio_processor.transcribe_audio(audio_file)
    return transcription.text


def get_structured_suggested_questions_with_context(telegram_id: int):
    try:
        user_language = get_user_language(telegram_id)
        conversation_list = get_conversation_list(telegram_id)
        if not conversation_list:
            return []
        prompt = f"""
       Suggest three relevant follow-up questions I might want to ask next based on our conversation history. The response should be a JSON object with a single key, "questions", whose value is a list containing exactly three elements. Each element should be a concise and relevant question in {user_language} language.
        """

        response = text_processor.generate_text_response(
            conversation_list + [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            stream=False,
            response_format={"type": "json_object"}
        )

        # Parse the JSON string if content is a string
        content = response.choices[0].message.content
        if isinstance(content, str):
            content = json.loads(content)

        return content["questions"]
    except Exception as e:
        print(f"Error generating suggested questions: {str(e)}")
        return []  # Return empty list instead of dict to match expected return type
