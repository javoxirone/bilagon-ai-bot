from typing import NoReturn
from database.repositories.conversation import Conversation
from exceptions.database import RelatedRecordDoesNotExist, DataTypeError, DBError
from exceptions.service import ServerError


def insert_conversation(telegram_id: int, role: str, content: str) -> NoReturn:
    try:
        db: Conversation = Conversation()
        db.add_conversation(telegram_id, role, content)
    except RelatedRecordDoesNotExist:
        raise
    except DataTypeError:
        raise
    except DBError:
        raise ServerError("Internal database error occurred while adding new conversation!")
