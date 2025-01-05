from typing import NoReturn
from data_types.db import UserDataType
from database.base import Database
from psycopg2.extensions import cursor as CursorType
from psycopg2 import (
    IntegrityError,
    OperationalError,
    DataError,
)
from exceptions.database import (
    UserAlreadyExistsError,
    DBError,
    DataTypeError, UserDoesNotExist, NoRecordsFound,
)


class User(Database):
    def __init__(self):
        super().__init__()

    def _serialize(self, user_data_raw: tuple[any, ...]) -> UserDataType:
        try:
            user_id: int = user_data_raw[0]
            telegram_id: int = user_data_raw[1]
            username: str = user_data_raw[2]
            first_name: str = user_data_raw[3]
            last_name: str = user_data_raw[4]
            created_at: str = user_data_raw[5]
            language: str = user_data_raw[6]

            return {
                "user_id": user_id,
                "telegram_id": telegram_id,
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "created_at": created_at,
                "language": language
            }
        except IndexError as e:
            raise ValueError("User data raw tuple does not contain the required number of elements") from e
        except TypeError as e:
            raise ValueError("Invalid data type encountered while processing user data") from e

    def get_raw_user_list(self) -> list[tuple[any, ...]]:
        try:
            with self as db_session:
                cursor: CursorType = db_session.conn.cursor()
                cursor.execute('SELECT * FROM users')
                user_list_raw: list[tuple[any, ...]] = cursor.fetchall()
                if not user_list_raw:
                    raise NoRecordsFound("There is no any users on the database")
                return user_list_raw
        except OperationalError:
            raise DBError()
        except DataError:
            raise DataTypeError()

    def get_serialized_user_list(self) -> list[UserDataType]:

        try:
            raw_user_list: list[tuple[any, ...]] = self.get_raw_user_list()
            serialized_user_list: list[UserDataType] = []
            for raw_user_data in raw_user_list:
                serialized_user_data: UserDataType = self._serialize(raw_user_data)
                serialized_user_list.append(serialized_user_data)
            return serialized_user_list
        except OperationalError:
            raise DBError()
        except DataError:
            raise DataTypeError()
        except NoRecordsFound:
            return []

    def get_raw_user(self, telegram_id: int) -> tuple[any, ...]:
        try:
            with self as db_session:
                cursor: CursorType = db_session.conn.cursor()
                cursor.execute('SELECT * FROM users WHERE telegram_id = %s', (telegram_id,))
                raw_user_data = cursor.fetchone()
                if not raw_user_data:
                    raise UserDoesNotExist(f"Provided telegram_id is {telegram_id}")
                return raw_user_data
        except OperationalError:
            raise DBError(f"Database operational error occurred while getting a user, telegram_id is {telegram_id}")
        except DataError:
            raise DataTypeError(
                f"Data type error occurred because of wrong data type used while fetching a user, telegram_id is {telegram_id}")

    def get_serialized_user(self, telegram_id: int) -> UserDataType:
        try:
            raw_user_data = self.get_raw_user(telegram_id)
            if not raw_user_data:
                raise UserDoesNotExist(f"Provided telegram_id is {telegram_id}")
            serialized_user_data: UserDataType = self._serialize(raw_user_data)
            return serialized_user_data
        except UserDoesNotExist:
            raise
        except DBError:
            raise
        except DataTypeError:
            raise

    def get_user_id(self, telegram_id: int) -> int:
        try:
            with self as db_session:
                cursor: CursorType = db_session.conn.cursor()
                cursor.execute("SELECT user_id FROM users WHERE telegram_id = %s", (telegram_id,))
                user_id = cursor.fetchone()
                if not user_id:
                    raise UserDoesNotExist(f"Provided telegram_id is {telegram_id}")
                return user_id[0]
        except OperationalError:
            raise DBError(f"Database operational error occurred while getting a user id, telegram_id is {telegram_id}")
        except DataError:
            raise DataTypeError(
                f"Data type error occurred because of wrong data type used while fetching a user id, telegram_id is {telegram_id}")

    def add_user(self, telegram_id: int, username: str, first_name: str, last_name: str, language: str) -> NoReturn:

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
            raise UserAlreadyExistsError(f"Provided telegram_id is {telegram_id}")
        except DataError:
            raise DataTypeError()
        except OperationalError:
            raise DBError()

    def user_exists(self, telegram_id: int) -> bool:

        try:
            with self as db_session:
                cursor: CursorType = db_session.conn.cursor()
                cursor.execute('''
                    SELECT COUNT(*)
                    FROM users
                    WHERE telegram_id = %s
                ''', (telegram_id,))
                count: int = cursor.fetchone()[0]
                return count > 0
        except OperationalError:
            raise DBError()
        except DataError:
            raise DataTypeError()

    def update_user_language(self, telegram_id: int, new_language: str) -> NoReturn:

        if not self.user_exists(telegram_id):
            raise UserDoesNotExist(f"Provided telegram_id is {telegram_id}")
        try:
            with self as db_session:
                cursor: CursorType = db_session.conn.cursor()
                cursor.execute('UPDATE users SET language = %s WHERE telegram_id = %s',
                               (new_language, telegram_id))
                db_session.conn.commit()
        except OperationalError:
            raise DBError()
        except DataError:
            raise DataTypeError()
