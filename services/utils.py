from datetime import datetime
from database.user import User


def format_datetime(dt) -> None | datetime:
    """
    This utility function gets datetime as an argument and returns either None or python datetime format.

    :param dt: datetime in string format.
    :return: None or python datetime format.
    """
    if dt:
        return datetime.strptime(dt.split(".")[0], "%Y-%m-%d %H:%M:%S").strftime(
            "%H:%M:%S %d.%m.%Y"
        )
    return None


def get_single_user(telegram_id: int) -> dict:
    """
    This utility function gets telegram_id and returns single user from database.

    :param telegram_id: Unique ID of the Telegram user.
    :return: Dictionary with user's information.
    """
    db = User()
    user = db.get_user_by_telegram_id(telegram_id)
    db.close()
    return user


def get_language_of_single_user(telegram_id: int) -> str:
    """
    This utility function extracts language of the single user by telegram_id.

    :param telegram_id: Unique ID of the Telegram user.
    :return: Language code (e.g. EN, RU, UZ)
    """
    user = get_single_user(telegram_id)
    return user["language"]
