from typing import Iterable

from psycopg2 import IntegrityError, OperationalError
from redis import DataError
from psycopg2.extensions import cursor as CursorType
from exceptions.db import UserAlreadyExistsError, DBError, DataTypeInsertError
from .base import Database


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
            raise UserAlreadyExistsError(telegram_id)
        except DataError:
            db_session.conn.rollback()
            raise DataTypeInsertError()
        except OperationalError:
            db_session.conn.rollback()
            raise DBError()

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
