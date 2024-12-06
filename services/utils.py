from database.user import User




def get_single_user(telegram_id: int) -> dict:
    """
    This utility function gets telegram_id and returns single user from database.

    :param telegram_id: Unique ID of the Telegram user.
    :return: Dictionary with user's information.
    """
    db = User()
    user: dict = db.get_user_by_telegram_id(telegram_id)
    db.close()
    return user


def get_language_of_single_user(telegram_id: int) -> str:
    """
    This utility function extracts language of the single user by telegram_id.

    :param telegram_id: Unique ID of the Telegram user.
    :return: Language code (e.g. EN, RU, UZ)
    """
    user: dict = get_single_user(telegram_id)
    language: str = user["language"]
    return language
