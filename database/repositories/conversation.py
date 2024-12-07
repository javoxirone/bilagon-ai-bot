from typing import NoReturn

from psycopg2 import DataError, OperationalError
from psycopg2.extensions import cursor as CursorType

from data_types.db import ConversationDataType
from database.base import Database
from database.repositories.user import User
from exceptions.database import UserDoesNotExist, RelatedRecordDoesNotExist, DBError, DataTypeError
from services.database.user import get_user_id_by_telegram_id


class Conversation(Database):
    def __init__(self):
        super().__init__()

    def _serialize(self, conversation_data_raw: tuple[any, ...]) -> ConversationDataType:
        """
        Serializes raw conversation data into a dictionary format with specified keys
        for role and content. The input is expected to be a tuple with at least two
        elements. This method ensures the conversation data is structured in a standard
        format, which can be used for further processing or storage.

        :param conversation_data_raw: A tuple where the first element is the role and
                                      the second is the content, representing parts of
                                      a conversation.
        :return: Serialized conversation data as a dictionary with 'role' and 'content'
                 keys.
        :raises ValueError: If 'conversation_data_raw' does not contain at least two
                            elements or contains invalid data types.
        """
        try:
            role: str = conversation_data_raw[0]
            content: str = conversation_data_raw[1]
            return {
                "role": role,
                "content": content
            }
        except IndexError as e:
            raise ValueError("User data raw tuple does not contain the required number of elements") from e
        except TypeError as e:
            raise ValueError("Invalid data type encountered while processing conversation data") from e

    def add_conversation(self, telegram_id: int, role: str, message: str) -> NoReturn:
        """
        Adds a conversation entry to the database associated with a specific user
        identified by their Telegram ID. The function first retrieves the user data
        based on the provided Telegram ID, then inserts a new conversation record
        into the database with the specified user role and message. The insertion
        operation or data retrieval may result in certain exceptions being raised
        if the data is invalid or the database operation fails.

        :param telegram_id: The unique identifier for a user in Telegram.
        :type telegram_id: int
        :param role: The role of the user in the conversation.
        :type role: str
        :param message: The message content of the conversation.
        :type message: str
        :raises RelatedRecordDoesNotExist: If the user with the given Telegram ID does
            not exist in the database.
        :raises DBError: If a database error occurs during the operation.
        :raises DataTypeError: If incorrect data types are provided or detected during
            the execution.
        """
        try:
            user_id: int = get_user_id_by_telegram_id(telegram_id)
        except UserDoesNotExist:
            raise RelatedRecordDoesNotExist(f"User with telegram_id {telegram_id} does not exist in the database.")

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

    def delete_all_conversations(self, telegram_id: int) -> NoReturn:
        """
        Deletes all conversation records from the database associated with a user identified by the given
        telegram_id. The method retrieves the user_id related to the telegram_id and deletes all records in
        the conversations table with this user_id. If the telegram_id does not correspond to any user, an
        exception is raised. Similarly, database operation errors are caught and raised as specific exceptions.

        :param telegram_id: Integer identifier of the user in the Telegram platform.

        :raises RelatedRecordDoesNotExist: If no user with the specified telegram_id exists in the database.
        :raises DataTypeError: If an incorrect data type is encountered during deletion.
        :raises DBError: If an internal database error occurs during the operation.

        :return: None
        """
        try:
            user_id: int = get_user_id_by_telegram_id(telegram_id)
        except UserDoesNotExist:
            raise RelatedRecordDoesNotExist(f"User with telegram_id {telegram_id} does not exist in the database.")
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

    def get_all_conversations(self, telegram_id: int) -> list[ConversationDataType]:
        """
        Fetch all conversations for a given user identified by their telegram ID. This method interfaces
        with the database to retrieve conversation records associated with the specified user, ordered by
        creation date.

        :param telegram_id: The unique identifier for a user on Telegram.
        :type telegram_id: int
        :return: A list containing serialized conversation data for the user.
        :rtype: list
        :raises RelatedRecordDoesNotExist: If the user ID associated with the telegram ID does not exist.
        :raises DBError: For internal database errors during the retrieval process.
        :raises DataTypeError: If incorrect data types are encountered during database operations.
        """
        try:
            user_id: int = get_user_id_by_telegram_id(telegram_id)
        except UserDoesNotExist:
            raise RelatedRecordDoesNotExist(f"User with telegram_id {telegram_id} does not exist in the database.")
        try:
            with self as db_session:
                cursor: CursorType = db_session.conn.cursor()
                cursor.execute('''
                    SELECT role, message FROM conversations
                    WHERE user_id = %s
                    ORDER BY created_at
                ''', (user_id,))
                conversations: list[tuple[any, ...]] = cursor.fetchall()
                conversation_list: list = []
                for conversation_data_raw in conversations:
                    conversation_data_serialized: ConversationDataType = self._serialize(conversation_data_raw)
                    conversation_list.append(conversation_data_serialized)
                return conversation_list
        except OperationalError:
            raise DBError(
                f"Internal database error occurred while getting all conversations related to the user with telegram_id {telegram_id}")
        except DataError:
            raise DataTypeError(
                f"Wrong data type was passed while getting all conversations related to the user with telegram_id {telegram_id}")


class Conversation2(Database):
    def __init__(self, db_name=None):
        super().__init__(db_name)

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS conversations (
                        conversation_id SERIAL PRIMARY KEY,
                        user_id INTEGER,
                        role CHAR(15),
                        message TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
                    )
                ''')
        self.conn.commit()

    def add_conversation(self, telegram_id, role, message):
        # Get user_id for the given telegram_id
        user_db = User()
        user_info = user_db.get_user_by_telegram_id(telegram_id)
        user_db.close()

        if user_info:
            user_id = user_info["user_id"]
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO conversations (user_id, role, message)
                VALUES (%s, %s, %s)
            ''', (user_id, role, message))
            self.conn.commit()
        else:
            print(f"User with telegram_id {telegram_id} not found.")

    def reset_conversations(self, telegram_id):
        # Get user_id for the given telegram_id
        user_db = User()
        user_info = user_db.get_user_by_telegram_id(telegram_id)
        user_db.close()
        if user_info:
            user_id = user_info["user_id"]
            cursor = self.conn.cursor()
            cursor.execute('DELETE FROM conversations WHERE user_id = %s', (user_id,))
            self.conn.commit()
            print(f"All conversations for telegram_id {telegram_id} have been reset.")
        else:
            print(f"User with telegram_id {telegram_id} not found.")

    def get_conversations_by_telegram_id(self, telegram_id):
        # Get user_id for the given telegram_id
        user_db = User()
        user_info = user_db.get_user_by_telegram_id(telegram_id)
        user_db.close()

        if user_info:
            user_id = user_info["user_id"]
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT role, message FROM conversations
                WHERE user_id = %s
                ORDER BY created_at
            ''', (user_id,))
            conversations = cursor.fetchall()

            conversation_list = []
            for conversation_data in conversations:
                role, message = conversation_data
                conversation_info = {
                    "role": role.strip(),
                    "content": message.strip()
                }
                print(conversation_info)
                conversation_list.append(conversation_info)

            return conversation_list
        else:
            print(f"User with telegram_id {telegram_id} not found.")
            return None
