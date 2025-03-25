from psycopg2 import IntegrityError

from data_types.database import UserDataType
from database.repositories.user import User
from exceptions.database import UserDoesNotExist, RelatedRecordDoesNotExist, DBError, DataTypeError
from aiogram.types import User as UserType


def update_user_model(telegram_id: int, model_name: str) -> None:
    user_db: User = User()
    try:
        user_db.update_user_fields(telegram_id, {"model_name": model_name})
    except (UserDoesNotExist, DBError, DataTypeError):
        raise
    finally:
        user_db.close()


def get_user_model_name(telegram_id: int) -> str:
    user_db: User = User()
    try:
        model_name: str = user_db.fetch_user_fields(telegram_id, "model_name")
        return model_name
    except (UserDoesNotExist, DBError, DataTypeError):
        raise
    finally:
        user_db.close()


def get_user_saved_conversation_mode(telegram_id: int) -> bool:
    user_db: User = User()
    try:
        mode: bool = user_db.fetch_user_fields(telegram_id, "saved_conversation_mode")
        return mode
    except (UserDoesNotExist, DBError, DataTypeError):
        raise
    finally:
        user_db.close()


def update_user_saved_conversation_mode(telegram_id: int, mode: bool):
    user_db: User = User()
    try:
        user_db.update_user_fields(telegram_id, {"saved_conversation_mode": mode})
    except (UserDoesNotExist, DBError, DataTypeError):
        raise
    finally:
        user_db.close()


def get_user_language(telegram_id: int) -> str:
    """
    This service gets serialized user data and returns language field.

    :param telegram_id: Unique telegram identification of the user.
    :type telegram_id: int

    :return: User's language preference.
    :rtype: str
    """

    user_db: User = User()
    try:
        language: str = user_db.fetch_user_fields(telegram_id, "language")
        return language
    except (UserDoesNotExist, DBError, DataTypeError):
        raise
    finally:
        user_db.close()


def get_user_by_telegram_id(telegram_id: int) -> UserDataType:
    """
    Retrieves a user's data using their Telegram ID. The function queries
    the database to find the user associated with the provided Telegram ID.
    If the user does not exist or if there are any database-related
    errors, appropriate exceptions are raised.

    :param telegram_id: The unique identifier associated with a Telegram user.
    :type telegram_id: int

    :return: User data corresponding to the specified Telegram ID.
    :rtype: UserDataType

    :raises RelatedRecordDoesNotExist: If no user exists with the given Telegram ID
    :raises DBError: If there is a database-related error during query execution
    :raises DataTypeError: If there is an error related to the data type of the returned user data
    """
    user_db: User = User()
    try:
        user_data: UserDataType = user_db.fetch_user_fields(telegram_id)
        return user_data
    except (UserDoesNotExist, DBError, DataTypeError):
        raise
    finally:
        user_db.close()


def get_user_id_by_telegram_id(telegram_id: int) -> int:
    """
    Retrieve the user ID associated with a given Telegram ID. The function
    interacts with a user database to obtain the corresponding user ID. In
    case of any specific exceptions related to user existence, database
    errors, or data type mismatches during the retrieval process, these
    exceptions will be raised to be handled by the caller.

    :param telegram_id: The unique Telegram identifier for the user.
    :type telegram_id: int

    :return: The ID of the user in the database system.
    :rtype: int

    :raises UserDoesNotExist: If no user is found with the given Telegram ID
    :raises DBError: If there is an issue with database connectivity or query
    :raises DataTypeError: If there is a data type mismatch in the retrieval process
    """
    user_db: User = User()
    try:
        user_id: int = user_db.fetch_user_fields(telegram_id, "user_id")
        return user_id
    except (UserDoesNotExist, DBError, DataTypeError):
        raise
    finally:
        user_db.close()


def update_user_language(telegram_id: int, language: str) -> None:
    user_db = User()
    try:
        user_db.update_user_fields(telegram_id, {"language": language})
    except (UserDoesNotExist, DBError, DataTypeError):
        raise
    finally:
        user_db.close()


def add_new_user(data: UserType) -> None:
    user_data = {
        "username": data.username,
        "first_name": data.first_name,
        "last_name": data.last_name,
        "language": 'en',
        "saved_conversation_mode": True
    }
    telegram_id: int = data.id
    user_db: User = User()
    try:
        user_db.add_user(telegram_id, user_data, False)
    except (IntegrityError, DBError, DataTypeError):
        raise
    finally:
        user_db.close()


def user_exists(telegram_id: int) -> bool:
    user_db: User = User()
    try:
        existence_status = user_db.user_exists(telegram_id)
        return existence_status
    except (UserDoesNotExist, DBError, DataTypeError):
        raise
    finally:
        user_db.close()
