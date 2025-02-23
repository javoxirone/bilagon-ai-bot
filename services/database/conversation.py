from database.repositories.conversation import Conversation
from exceptions.database import RelatedRecordDoesNotExist, DataTypeError, DBError
from exceptions.service import ServerError


def save_conversation(telegram_id: int, role: str, content: str) -> None:
    try:
        db: Conversation = Conversation()
        db.add_conversation(telegram_id, role, content)
    except RelatedRecordDoesNotExist:
        raise
    except DataTypeError:
        raise
    except DBError:
        raise ServerError("Internal database error occurred while adding new conversation!")


def get_conversation_list(telegram_id: int) -> list:
    try:
        db: Conversation = Conversation()
        conversation_list = db.get_serialized_conversation_list(telegram_id)
        return conversation_list
    except RelatedRecordDoesNotExist:
        raise
    except DataTypeError:
        raise
    except DBError:
        raise ServerError("Internal database error occurred while adding new conversation!")

def delete_all_user_conversations(telegram_id: int) -> None:
    try:
        db: Conversation = Conversation()
        db.delete_all_conversations(telegram_id)
    except RelatedRecordDoesNotExist:
        raise
    except DataTypeError:
        raise
    except DBError:
        raise ServerError("Internal database error occurred while adding new conversation!")