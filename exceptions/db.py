class DBError(Exception):
    """
    DBError exception is raised when Operational Error occurs.
    """

    def __init__(self, message: str = "No additional message"):
        """
        Initialize the custom DBError exception object.

        :param message: Additional error message.
        :type message: str
        """
        super().__init__(f"Something went wrong while operating with database ({message})")


class UserAlreadyExistsError(Exception):
    """
    UserAlreadyExistsError exception is raised when a user with certain telegram_id already exists in the database.
    """

    def __init__(self, message: str = "No additional message"):
        """
        Initialize the custom UserAlreadyExistsError exception object.

        :param message: Additional error message.
        :type message: str
        """
        super().__init__(f"User already exists({message})")


class DataTypeInsertError(Exception):
    """
    DataTypeInsertError exception is raised when you try to insert a data that violates the data type constraints.
    """

    def __init__(self, message: str = "No additional message"):
        """
        Initialize the custom DataTypeInsertError exception object.

        :param message: Additional error message.
        :type message: str
        """
        super().__init__(f"Could not insert data because of data type violation ({message})")


class UserDoesNotExist(Exception):
    """
    UserDoesNotExist exception is raised when a user with certain telegram_id does not exist in the database.
    """

    def __init__(self, message: str = "No additional message"):
        """
        Initialize the custom UserDoesNotExist exception object.

        :param message: Additional error message.
        :type message: str
        """
        super().__init__(f"User does not exist ({message})")
