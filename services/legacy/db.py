from database.repositories.user import User
from aiogram.types import User as UserType
from exceptions.service import ServerError
from exceptions.database import (
    UserAlreadyExistsError,
    DataTypeError,
    DBError,
)


def check_if_user_exists(telegram_id: int) -> bool:
    """
    Checks if a user exists in the database using the provided Telegram ID.

    This function attempts to connect to the database and determine whether
    a user with the specified Telegram ID exists. It handles database errors
    by raising a server-specific error, ensuring that any underlying issues
    related to the database or data types are not exposed directly.

    :param telegram_id: The unique Telegram ID of the user to be checked.
    :type telegram_id: int
    :return: A boolean indicating whether the user exists (True) or not (False).
    :rtype: bool
    :raises ServerError: If there is an internal database error or a data
                         type insert error occurs.
    """
    try:
        db: User = User()
        status: bool = db.user_exists(telegram_id)
        return status
    except DBError:
        raise ServerError("Internal database error!")
    except DataTypeError:
        raise ServerError("Data type insert error!")


def add_new_user(data: UserType) -> None:
    """
    Add a new user to the database.

    This function takes user data and attempts to add a new user to the database.
    If the user already exists or if there are any issues with inserting data
    into the database, a server error will be raised.

    :param data: The user data required to add a new user.
    :type data: UserType
    :raises ServerError: If the user already exists, there is an error inserting
        the data type, or an internal database error occurs.
    """
    telegram_id: int = data.id
    username: str = data.username
    first_name: str = data.first_name
    last_name: str = data.last_name
    lang: str = "en"
    try:
        db: User = User()
        db.add_user(telegram_id, username, first_name, last_name, lang)
    except UserAlreadyExistsError as e:
        raise ServerError("Such user already exists!")
    except DataTypeError:
        raise ServerError("Data type insert error!")
    except DBError:
        raise ServerError("Internal database error!")
