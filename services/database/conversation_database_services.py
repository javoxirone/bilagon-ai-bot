from database.repositories.conversation import Conversation
from exceptions.database import RelatedRecordDoesNotExist, DataTypeError, DBError
from exceptions.service import ServerError


def save_conversation(telegram_id: int, role: str, content: str) -> None:
    conversation_db: Conversation = Conversation()
    try:
        conversation_db.add_conversation(telegram_id, role, content)
    except RelatedRecordDoesNotExist:
        conversation_db.close()
        raise
    except DataTypeError:
        conversation_db.close()
        raise
    except DBError:
        conversation_db.close()
        raise ServerError("Internal database error occurred while adding new conversation!")
    finally:
        conversation_db.close()


def get_conversation_list(telegram_id: int) -> list:
    conversation_db: Conversation = Conversation()
    try:
        conversation_list = conversation_db.get_serialized_conversation_list(telegram_id)
        return conversation_list
    except RelatedRecordDoesNotExist:
        conversation_db.close()
        raise
    except DataTypeError:
        conversation_db.close()
        raise
    except DBError:
        conversation_db.close()
        raise ServerError("Internal database error occurred while adding new conversation!")
    finally:
        conversation_db.close()

def delete_all_user_conversations(telegram_id: int) -> None:
    conversation_db: Conversation = Conversation()
    try:
        conversation_db.delete_all_conversations(telegram_id)
    except RelatedRecordDoesNotExist:
        conversation_db.close()
        raise
    except DataTypeError:
        conversation_db.close()
        raise
    except DBError:
        conversation_db.close()
        raise ServerError("Internal database error occurred while adding new conversation!")
    finally:
        conversation_db.close()