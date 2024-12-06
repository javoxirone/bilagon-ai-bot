from typing import TypedDict, Iterable, Union

from types.db import UserDataType
from .base import Database
from psycopg2.extensions import cursor as CursorType
from psycopg2 import (
    IntegrityError,
    OperationalError,
    DataError,
)
from exceptions.db import (
    UserAlreadyExistsError,
    DBError,
    DataTypeInsertError, UserDoesNotExist,
)


class User(Database):
    def __init__(self):
        super().__init__()

    def add_user(self, telegram_id: int, username: str, first_name: str, last_name: str, language: str) -> None:
        """
        Adds a new user to the database with the provided details. The operation
        will attempt to insert a new record into the 'users' table. If the
        insertion leads to a data integrity violation, e.g., duplicate telegram_id,
        a UserAlreadyExistsError is raised. This method performs database rollback
        in case of any errors to maintain database consistency.

        :param telegram_id: The unique identifier for the user in Telegram.
        :type telegram_id: int
        :param username: The username of the user.
        :type username: str
        :param first_name: The first name of the user.
        :type first_name: str
        :param last_name: The last name of the user.
        :type last_name: str
        :param language: The preferred language of the user.
        :type language: str
        :raises UserAlreadyExistsError: If a user with the given telegram_id already exists.
        :raises DataTypeInsertError: If there is an issue with the data type during insertion.
        :raises DBError: For any general operational errors encountered during the insertion.

        Examples:
            >>> db = User()
            >>> db.add_user(123456789, "john_smith", "John", "Smith", "en")
            None
        """

        try:
            with self as db_session:
                cursor: CursorType = db_session.conn.cursor()
                cursor.execute('''
                            INSERT INTO users (
                                telegram_id,
                                username,
                                first_name,
                                last_name,
                                language
                            )
                            VALUES (%s, %s, %s, %s, %s);
                        ''', (telegram_id,
                              username,
                              first_name,
                              last_name,
                              language,))
                db_session.conn.commit()
        except IntegrityError:
            db_session.conn.rollback()
            raise UserAlreadyExistsError(f"Provided telegram_id is {telegram_id}")
        except DataError:
            db_session.conn.rollback()
            raise DataTypeInsertError()
        except OperationalError:
            db_session.conn.rollback()
            raise DBError()

    def get_user(self, telegram_id: int) -> UserDataType:
        """
        Retrieve user information from the database using the given telegram ID.

        This method queries the database for a user with the specified telegram ID.
        If the user is found, their data is returned in a dictionary format.
        If the user does not exist or any database errors occur during the process,
        appropriate exceptions are raised.

        :param telegram_id: Unique identifier for the user in the telegram system
        :type telegram_id: int
        :return: A dictionary containing user information if found
        :rtype: UserDataType
        :raises UserDoesNotExist: If no user is found with the provided telegram ID
        :raises DBError: If an operational error occurs within the database
        :raises DataTypeInsertError: If a data error occurs while inserting the data type
        
        Examples:
            >>> db = User()
            >>> db.get_user(123456789)
            {
                "user_id": 1,
                "telegram_id": 123456789,
                "username": "john_smith",
                "first_name": "John",
                "last_name": "Smith",
                "created_at": "2023-03-15T12:34:56",
                "language": "en"
            }
        """
        try:
            with self as db_session:
                cursor: CursorType = db_session.conn.cursor()
                cursor.execute('SELECT * FROM users WHERE telegram_id = %s', (telegram_id,))
                user_data = cursor.fetchone()
                if not user_data:
                    raise UserDoesNotExist(f"Provided telegram_id is {telegram_id}")
                user_info: UserDataType = {
                    "user_id": user_data[0],
                    "telegram_id": user_data[1],
                    "username": user_data[2],
                    "first_name": user_data[3],
                    "last_name": user_data[4],
                    "created_at": user_data[5],
                    "language": user_data[6]
                }
                return user_info
        except OperationalError:
            raise DBError()
        except DataError:
            raise DataTypeInsertError()

    def get_user_list(self):
        """
        Retrieves a list of users from the database. The users are fetched from the
        'users' table and the raw data is transformed into a list of dictionaries,
        each representing a user with specific fields.

        The function attempts to establish a database session and execute an SQL
        query to fetch all records from the 'users' table. Each record is then
        serialized into a dictionary format suitable for further processing or
        usage. If the users list is empty, an empty list is returned. In the event
        of database operation errors, specific exceptions are raised to indicate
        the type of failure encountered.

        :return: A list of dictionaries, each containing user data from the database.
        :rtype: list[UserDataType]

        :raises DBError: If there is an error establishing a database connection
                         or executing the database operation.
        :raises DataTypeInsertError: If there is an error related to data types
                                     during data retrieval or processing.
        """
        try:
            with self as db_session:
                cursor: CursorType = db_session.conn.cursor()
                cursor.execute('SELECT * FROM users')
                user_list_raw: list[tuple[any, ...]] = cursor.fetchall()
                user_list_serialized: list[UserDataType] = []

                if not user_list_raw:
                    return []

                for user_data_raw in user_list_raw:
                    user_data_serialized: UserDataType = {
                        "user_id": user_data_raw[0],
                        "telegram_id": user_data_raw[1],
                        "username": user_data_raw[2],
                        "first_name": user_data_raw[3],
                        "last_name": user_data_raw[4],
                        "created_at": user_data_raw[5],
                        "language": user_data_raw[6]
                    }
                    user_list_serialized.append(user_data_serialized)
                return user_list_serialized
        except OperationalError:
            raise DBError()
        except DataError:
            raise DataTypeInsertError()

    def user_exists(self, telegram_id: int) -> bool:
        """
        Determines whether a user with a given Telegram ID exists within
        the database. This method executes a query to check the presence
        of the user and returns a boolean result based on the count.

        :param telegram_id: The unique identifier for a Telegram user.
        :type telegram_id: int
        :return: True if the user exists, otherwise False.
        :rtype: bool
        :raises DBError: If there is an operational error during database
                         communication.
        :raises DataTypeInsertError: If there is an issue with the data
                                     type during the insert operation.

        Examples:
            >>> db = User()
            >>> db.user_exists(123456789)
            True

            >>> db = User()
            >>> db.user_exists(987654321)
            False
        """
        try:
            with self as db_session:
                cursor: CursorType = db_session.conn.cursor()
                cursor.execute('''
                    SELECT COUNT(*)
                    FROM users
                    WHERE telegram_id = %s
                ''', (telegram_id,))
                count = cursor.fetchone()[0]
                return count > 0
        except OperationalError:
            raise DBError()
        except DataError:
            raise DataTypeInsertError()


class User2(Database):
    def __init__(self, db_name=None):
        super().__init__(db_name)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(f"An exception occurred: {exc_type}, {exc_val}, {exc_tb}")
        self.close()
        return False

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                telegram_id BIGINT UNIQUE,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                language TEXT
            )
        ''')
        self.conn.commit()

    def add_user(self, telegram_id, username, first_name, last_name, language):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO users (telegram_id, username, first_name, last_name, language)
            VALUES (%s, %s, %s, %s, %s)
        ''', (telegram_id, username, first_name, last_name, language))
        self.conn.commit()

    def get_user_by_telegram_id(self, telegram_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE telegram_id = %s', (telegram_id,))
        user_data = cursor.fetchone()
        print(user_data)

        if user_data:
            user_info = {
                "user_id": user_data[0],
                "telegram_id": user_data[1],
                "username": user_data[2],
                "first_name": user_data[3],
                "last_name": user_data[4],
                "created_at": user_data[5],
                "language": user_data[6]
            }
            return user_info
        else:
            return None

    def get_all_users(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()

        user_info_list = []
        for user_data in users:
            user_info = {
                "telegram_id": user_data[1],
                "username": user_data[2],
                "first_name": user_data[3],
                "last_name": user_data[4],
                "created_at": user_data[5],
                "language": user_data[6]
            }
            user_info_list.append(user_info)

        return user_info_list

    def change_language(self, telegram_id, new_language):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE users SET language = %s WHERE telegram_id = %s',
                       (new_language, telegram_id))
        self.conn.commit()

    def user_exists(self, telegram_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users WHERE telegram_id = %s', (telegram_id,))
        count = cursor.fetchone()[0]
        return count > 0
