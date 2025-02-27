from database.repositories.conversation import Conversation

def add_message_of_user_to_conversation(telegram_id:int, text:str) -> None:
    conversation_db = Conversation()
    conversation_db.add_conversation(telegram_id, "user", text)
    conversation_db.close()

def add_message_of_assistant_to_conversation(telegram_id:int, text:str) -> None:
    conversation_db = Conversation()
    conversation_db.add_conversation(telegram_id, "assistant", text)
    conversation_db.close()

def get_conversations_of_single_user(telegram_id:int) -> dict:
    conversation_db = Conversation()
    conversations = conversation_db.get_conversations_by_telegram_id(telegram_id)
    conversation_db.close()
    return conversations