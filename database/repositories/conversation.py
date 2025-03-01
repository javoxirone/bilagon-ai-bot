from psycopg2 import DataError, OperationalError
from data_types.database import ConversationDataType
from database.base import Database
from exceptions.database import (
    UserDoesNotExist,
    RelatedRecordDoesNotExist,
    DBError,
    DataTypeError,
)
from services.database.user_database_services import get_user_id_by_telegram_id


class Conversation(Database):
    """
    Repository for managing user conversations.
    """

    def __init__(self):
        """
        Initialize Conversation repository.
        """
        super().__init__()

    def _serialize(self, conversation_data_raw: tuple[any, ...]) -> ConversationDataType:
        """
        Convert raw conversation data to a structured dictionary.
        """
        try:
            role: str = conversation_data_raw[0]
            content: str = conversation_data_raw[1]
            return {
                "role": role.strip(),
                "content": content
            }
        except IndexError as e:
            raise ValueError("Conversation data raw tuple does not contain the required number of elements") from e
        except TypeError as e:
            raise ValueError("Invalid data type encountered while processing conversation data") from e

    def _get_user_id(self, telegram_id: int) -> int:
        """
        Get the internal user ID by telegram ID.
        """
        try:
            user_id: int = get_user_id_by_telegram_id(telegram_id)
            return user_id
        except UserDoesNotExist:
            raise RelatedRecordDoesNotExist(f"User with telegram_id {telegram_id} does not exist in the database.")

    def add_conversation(self, telegram_id: int, role: str, message: str) -> None:
        """
        Add a new conversation entry for a user.
        """
        try:
            user_id: int = self._get_user_id(telegram_id)
        except RelatedRecordDoesNotExist:
            raise

        try:
            cursor = self.execute_query(
                '''
                INSERT INTO conversations (user_id, role, message)
                VALUES (%s, %s, %s)
                ''',
                (user_id, role, message)
            )
            cursor.close()
            self.commit()
        except DataError as e:
            self.rollback()
            raise DataTypeError(
                f"Wrong data type was passed while adding a new conversation for a user with telegram_id {telegram_id}: {str(e)}")
        except OperationalError as e:
            self.rollback()
            raise DBError(
                f"Internal database error occurred while adding a new conversation for a user with telegram_id {telegram_id}: {str(e)}")
        except Exception as e:
            self.rollback()
            raise DBError(f"Error adding conversation: {str(e)}")

    def delete_all_conversations(self, telegram_id: int) -> None:
        """
        Delete all conversation entries for a user.
        """
        try:
            user_id: int = self._get_user_id(telegram_id)
        except RelatedRecordDoesNotExist:
            raise

        try:
            cursor = self.execute_query(
                'DELETE FROM conversations WHERE user_id = %s',
                (user_id,)
            )
            cursor.close()
            self.commit()
        except DataError as e:
            self.rollback()
            raise DataTypeError(
                f"Wrong data type was passed while deleting all conversations related to the user with telegram_id {telegram_id}: {str(e)}")
        except OperationalError as e:
            self.rollback()
            raise DBError(
                f"Internal database error occurred while deleting all conversations related to the user with telegram_id {telegram_id}: {str(e)}")
        except Exception as e:
            self.rollback()
            raise DBError(f"Error deleting conversations: {str(e)}")

    def get_raw_conversation_list(self, telegram_id: int) -> list[tuple[any, ...]]:
        """
        Get a list of all conversations for a user in raw format.
        """
        try:
            user_id: int = self._get_user_id(telegram_id)
        except RelatedRecordDoesNotExist:
            raise

        try:
            cursor = self.execute_query(
                '''
                SELECT role, message FROM conversations
                WHERE user_id = %s
                ORDER BY created_at
                ''',
                (user_id,)
            )
            conversations: list[tuple[any, ...]] = cursor.fetchall()
            cursor.close()

            if not conversations:
                return []

            return conversations
        except OperationalError as e:
            self.rollback()
            raise DBError(
                f"Internal database error occurred while getting all conversations related to the user with telegram_id {telegram_id}: {str(e)}")
        except DataError as e:
            self.rollback()
            raise DataTypeError(
                f"Wrong data type was passed while getting all conversations related to the user with telegram_id {telegram_id}: {str(e)}")
        except Exception as e:
            self.rollback()
            raise DBError(f"Error retrieving conversations: {str(e)}")
        finally:
            self.commit()

    def get_serialized_conversation_list(self, telegram_id: int) -> list[ConversationDataType]:
        """
        Get a list of all conversations for a user in serialized format.
        """
        try:
            conversations = self.get_raw_conversation_list(telegram_id)
            conversation_list: list[ConversationDataType] = []

            for conversation_data_raw in conversations:
                conversation_data_serialized: ConversationDataType = self._serialize(conversation_data_raw)
                conversation_list.append(conversation_data_serialized)

            return conversation_list
        except RelatedRecordDoesNotExist:
            raise
        except (DBError, DataTypeError):
            raise