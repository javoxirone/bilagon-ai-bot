from data_types.db import UserDataType
from database.repositories.user import User
from exceptions.database import UserDoesNotExist, RelatedRecordDoesNotExist, DBError, DataTypeError


def get_user_by_telegram_id(telegram_id: int) -> UserDataType:
    """
    Retrieves a user's data using their Telegram ID. The function queries
    the database to find the user associated with the provided Telegram ID.
    If the user does not exist or if there are any database-related
    errors, appropriate exceptions are raised.

    :param telegram_id: The unique identifier associated with a Telegram user
    :type telegram_id: int
    :return: User data corresponding to the specified Telegram ID
    :rtype: UserDataType
    :raises RelatedRecordDoesNotExist: If no user exists with the given Telegram ID
    :raises DBError: If there is a database-related error during query execution
    :raises DataTypeError: If there is an error related to the data type of the returned user data
    """
    try:
        user_db: User = User()
        user_data: UserDataType = user_db.get_user(telegram_id)
        return user_data
    except UserDoesNotExist:
        raise
    except DBError:
        raise
    except DataTypeError:
        raise


def get_user_id_by_telegram_id(telegram_id: int) -> int:
    """
    Retrieve the user ID associated with a given Telegram ID. The function
    interacts with a user database to obtain the corresponding user ID. In
    case of any specific exceptions related to user existence, database
    errors, or data type mismatches during the retrieval process, these
    exceptions will be raised to be handled by the caller.

    :param telegram_id: The unique Telegram identifier for the user
    :return: The ID of the user in the database system
    :raises UserDoesNotExist: If no user is found with the given Telegram ID
    :raises DBError: If there is an issue with database connectivity or query
    :raises DataTypeError: If there is a data type mismatch in the retrieval process
    """
    try:
        user_db: User = User()
        user_id: int = user_db.get_user_id(telegram_id)
        return user_id
    except UserDoesNotExist:
        raise
    except DBError:
        raise
    except DataTypeError:
        raise