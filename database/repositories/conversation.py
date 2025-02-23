from psycopg2 import DataError, OperationalError
from psycopg2.extensions import cursor as CursorType
from data_types.db import ConversationDataType
from database.base import Database
from exceptions.database import UserDoesNotExist, RelatedRecordDoesNotExist, DBError, DataTypeError
from services.database.user import get_user_id_by_telegram_id


class Conversation(Database):
    def __init__(self):
        super().__init__()

    def _serialize(self, conversation_data_raw: tuple[any, ...]) -> ConversationDataType:
        try:
            role: str = conversation_data_raw[0]
            content: str = conversation_data_raw[1]
            return {
                "role": role.strip(),
                "content": content
            }
        except IndexError as e:
            raise ValueError("User data raw tuple does not contain the required number of elements") from e
        except TypeError as e:
            raise ValueError("Invalid data type encountered while processing conversation data") from e

    def _get_user_id(self, telegram_id: int) -> int:
        try:
            user_id: int = get_user_id_by_telegram_id(telegram_id)
            return user_id
        except UserDoesNotExist:
            raise RelatedRecordDoesNotExist(f"User with telegram_id {telegram_id} does not exist in the database.")

    def add_conversation(self, telegram_id: int, role: str, message: str) -> None:
        try:
            user_id: int = self._get_user_id(telegram_id)
        except RelatedRecordDoesNotExist:
            raise
        try:
            with self as db_session:
                cursor: CursorType = db_session.conn.cursor()
                cursor.execute('''
                    INSERT INTO conversations (user_id, role, message)
                    VALUES (%s, %s, %s)
                ''', (user_id, role, message))
                db_session.conn.commit()
        except DataError:
            raise DataTypeError(
                f"Wrong data type was passed while adding a new conversation for a user with telegram_id {telegram_id}")
        except OperationalError:
            raise DBError(
                f"Internal database error occurred while adding a new conversation for a user with telegram_id {telegram_id}")

    def delete_all_conversations(self, telegram_id: int) -> None:
        try:
            user_id: int = self._get_user_id(telegram_id)
        except RelatedRecordDoesNotExist:
            raise
        try:
            with self as db_session:
                cursor: CursorType = db_session.conn.cursor()
                cursor.execute('DELETE FROM conversations WHERE user_id = %s', (user_id,))
                db_session.conn.commit()
        except DataError:
            raise DataTypeError(
                f"Wrong data type was passed while deleting all conversations related to the user with telegram_id {telegram_id}")
        except OperationalError:
            raise DBError(
                f"Internal database error occurred while deleting all conversations related to the user with telegram_id {telegram_id}")

    def get_raw_conversation_list(self, telegram_id: int) -> list[tuple[any, ...]]:
        try:
            user_id: int = self._get_user_id(telegram_id)
        except RelatedRecordDoesNotExist:
            raise

        try:
            with self as db_session:
                cursor: CursorType = db_session.conn.cursor()
                cursor.execute('''
                    SELECT role, message FROM conversations
                    WHERE user_id = %s
                    ORDER BY created_at
                ''', (user_id,))
                conversations: list[tuple[any, ...]] = cursor.fetchall()
                return conversations
        except OperationalError:
            raise DBError(
                f"Internal database error occurred while getting all conversations related to the user with telegram_id {telegram_id}")
        except DataError:
            raise DataTypeError(
                f"Wrong data type was passed while getting all conversations related to the user with telegram_id {telegram_id}")

    def get_serialized_conversation_list(self, telegram_id: int) -> list[ConversationDataType]:
        try:
            conversations = self.get_raw_conversation_list(telegram_id)
            conversation_list: list[ConversationDataType] = []
            for conversation_data_raw in conversations:
                conversation_data_serialized: ConversationDataType = self._serialize(conversation_data_raw)
                conversation_list.append(conversation_data_serialized)
            return conversation_list
        except RelatedRecordDoesNotExist:
            raise
        except OperationalError:
            raise DBError(
                f"Internal database error occurred while getting all conversations related to the user with telegram_id {telegram_id}")
        except DataError:
            raise DataTypeError(
                f"Wrong data type was passed while getting all conversations related to the user with telegram_id {telegram_id}")
