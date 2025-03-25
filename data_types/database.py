from typing import TypedDict


class UserDataType(TypedDict):
    user_id: int
    telegram_id: int
    username: str
    first_name: str
    last_name: str
    created_at: str
    language: str
    saved_conversation_mode: bool


class ConversationDataType(TypedDict):
    role: str
    content: str
