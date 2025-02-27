from data_types.db import UserDataType
from database.base import Database
from psycopg2 import (
    IntegrityError,
    OperationalError,
    DataError,
)
from exceptions.database import (
    UserAlreadyExistsError,
    DBError,
    UserDoesNotExist, NoRecordsFound,
)


class User(Database):
    def __init__(self):
        """
        Initialize User repository.
        """
        super().__init__()

    def _serialize(self, user_data_raw: tuple[any, ...]) -> UserDataType:
        """
        Convert raw user data to a structured dictionary.
        """
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
        """
        Get a list of all users in raw format.
        """
        try:
            cursor = self.execute_query('SELECT * FROM users')
            user_list_raw = cursor.fetchall()
            cursor.close()

            if not user_list_raw:
                raise NoRecordsFound("There are no users in the database")

            return user_list_raw
        except (OperationalError, DataError) as e:
            raise DBError(f"Database error while getting user list: {str(e)}")
        finally:
            self.commit()

    def get_serialized_user_list(self) -> list[UserDataType]:
        """
        Get a list of all users in serialized format.
        """
        try:
            raw_user_list = self.get_raw_user_list()
            serialized_user_list = []

            for raw_user_data in raw_user_list:
                serialized_user_data = self._serialize(raw_user_data)
                serialized_user_list.append(serialized_user_data)

            return serialized_user_list
        except NoRecordsFound:
            return []

    def get_raw_user(self, telegram_id: int) -> tuple[any, ...]:
        """
        Get raw user data by telegram ID.
        """
        try:
            cursor = self.execute_query(
                'SELECT * FROM users WHERE telegram_id = %s',
                (telegram_id,)
            )
            raw_user_data = cursor.fetchone()
            cursor.close()

            if not raw_user_data:
                raise UserDoesNotExist(f"User with telegram_id {telegram_id} does not exist")

            return raw_user_data
        finally:
            self.commit()

    def get_serialized_user(self, telegram_id: int) -> UserDataType:
        """
        Get serialized user data by telegram ID.
        """
        raw_user_data = self.get_raw_user(telegram_id)
        return self._serialize(raw_user_data)

    def get_user_id(self, telegram_id: int) -> int:
        """
        Get the internal user ID by telegram ID.
        """
        try:
            cursor = self.execute_query(
                "SELECT user_id FROM users WHERE telegram_id = %s",
                (telegram_id,)
            )
            user_id = cursor.fetchone()
            cursor.close()

            if not user_id:
                raise UserDoesNotExist(f"User with telegram_id {telegram_id} does not exist")

            return user_id[0]
        finally:
            self.commit()

    def add_user(self, telegram_id: int, username: str, first_name: str, last_name: str, language: str) -> None:
        """
        Add a new user to the database.
        """
        try:
            cursor = self.execute_query(
                '''
                INSERT INTO users (
                    telegram_id,
                    username,
                    first_name,
                    last_name,
                    language
                )
                VALUES (%s, %s, %s, %s, %s);
                ''',
                (telegram_id, username, first_name, last_name, language)
            )
            cursor.close()
            self.commit()
        except IntegrityError:
            self.rollback()
            raise UserAlreadyExistsError(f"User with telegram_id {telegram_id} already exists")

    def user_exists(self, telegram_id: int) -> bool:
        """
        Check if a user exists by telegram ID.
        """
        try:
            cursor = self.execute_query(
                '''
                SELECT COUNT(*)
                FROM users
                WHERE telegram_id = %s
                ''',
                (telegram_id,)
            )
            count = cursor.fetchone()[0]
            cursor.close()
            self.commit()
            return count > 0
        except Exception as e:
            self.rollback()
            raise DBError(f"Error checking if user exists: {str(e)}")

    def update_user_language(self, telegram_id: int, new_language: str) -> None:
        """
        Update a user's language preference.
        """
        if not self.user_exists(telegram_id):
            raise UserDoesNotExist(f"User with telegram_id {telegram_id} does not exist")

        try:
            cursor = self.execute_query(
                'UPDATE users SET language = %s WHERE telegram_id = %s',
                (new_language, telegram_id)
            )
            cursor.close()
            self.commit()
        except Exception as e:
            self.rollback()
            raise DBError(f"Error updating user language: {str(e)}")
