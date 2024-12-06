from datetime import datetime


def format_datetime(dt: str) -> None | str:
    """
    This utility function gets datetime as an argument and returns either None or python datetime format.

    :param dt: datetime in string format (2022-12-31 23:59:59.123456).
    :return: datetime in string format (23:59:59 31.12.2022).
    :return: None.
    """
    if dt:
        return datetime.strptime(dt.split(".")[0], "%Y-%m-%d %H:%M:%S").strftime(
            "%H:%M:%S %d.%m.%Y"
        )
    return None
