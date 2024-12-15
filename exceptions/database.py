class DBError(Exception):
    """
    A custom exception class for handling database-related errors.

    This class is designed to provide a specific exception for database
    operations, allowing for more precise error handling and debugging.
    It can be initialized with an optional error message that provides
    additional context about the error.
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
    Exception raised when an attempt is made to create a user that already
    exists in the system.

    This custom exception should be used in cases where user creation
    operations may conflict with existing users, ensuring clear and specific
    error handling for such occurrences.
    """

    def __init__(self, message: str = "No additional message"):
        """
        Initialize the custom UserAlreadyExistsError exception object.

        :param message: Additional error message.
        :type message: str
        """
        super().__init__(f"User already exists({message})")


class DataTypeError(Exception):
    """
    Custom exception class for handling data type violations.

    This exception is raised when an attempt to insert data violates
    the expected data type constraints. It extends the base Exception
    class and provides additional context through an error message.

    Usage of this exception should be considered when implementing
    data validation logic to ensure data types meet the required
    specifications.
    """

    def __init__(self, message: str = "No additional message"):
        """
        Initialize the custom DataTypeError exception object.

        :param message: Additional error message.
        :type message: str
        """
        super().__init__(f"Could not insert data because of data type violation ({message})")


class UserDoesNotExist(Exception):
    """
    Represents a custom exception used when a user is not found in the system.

    This exception is intended to be raised when operations that require
    a specific user fail to locate him/her in the database or any relevant
    data source. The exception allows for an optional custom message to
    provide additional context or information about the failure scenario.
    """

    def __init__(self, message: str = "No additional message"):
        """
        Initialize the custom UserDoesNotExist exception object.

        :param message: Additional error message.
        :type message: str
        """
        super().__init__(f"User does not exist ({message})")


class RelatedRecordDoesNotExist(Exception):
    """
    Initialize the custom RelatedRecordDoesNotExist exception object.

    This exception is raised when an attempt is made to access a
    related record that does not exist in the database. It extends
    the base Exception class and allows for an additional message
    to be provided for more context.
    """

    def __init__(self, message: str = "No additional message"):
        """
        Initialize the custom RelatedRecordDoesNotExist exception object.

        :param message: Additional error message.
        :type message: str
        """
        super().__init__(f"Related record does not exist ({message})")


class RollbackError(Exception):
    """
    Exception raised when a database rollback operation fails.

    RollbackError is a custom exception class used to indicate failure during
    a database rollback operation. It provides additional context by optionally
    storing the original exception that caused the rollback to fail.
    """

    def __init__(self, message: str = "Database rollback operation failed.",
                 original_exception: Exception | None = None):
        """
        Represents an error that occurs during a database rollback operation. This
        exception can be used to encapsulate detailed information about the rollback
        failure, including an optional original exception that led to this error.

        :param message: A descriptive message indicating the nature of the rollback
                        error. Defaults to "Database rollback operation failed."
        :type message: str
        :param original_exception: The original exception that caused the rollback
                                   to fail, if available. This provides additional
                                   context for debugging purposes.
        :type original_exception: Exception or None
        """
        super().__init__(message)
        self.original_exception = original_exception

    def __str__(self):
        if self.original_exception:
            return f"{super().__str__()} (Original exception: {self.original_exception})"
        return super().__str__()


class CommitError(Exception):
    """
    Represents an error that occurs during a database commit operation.

    This exception is raised when a commit operation to a database fails. It
    can encapsulate an optional original exception that was the cause of the
    commit failure, allowing for easier debugging and logging.
    """

    def __init__(self, message: str = "Database commit operation failed.", original_exception: Exception | None = None):
        """
        Represents an exception that is raised specifically when a database commit
        operation fails. This exception extends the base Exception class to provide
        more context regarding commit failures, including an optional message and
        an original underlying exception, if any.

        :param message: A description of the error that occurred. Defaults to
                        "Database commit operation failed." if not provided.
        :type message: str
        :param original_exception: The original exception that caused the commit to
                                   fail, if available. This is optional and can be
                                   set to None.
        :type original_exception: Exception or None
        """
        super().__init__(message)
        self.original_exception = original_exception

    def __str__(self):
        if self.original_exception:
            return f"{super().__str__()} (Original exception: {self.original_exception})"
        return super().__str__()


class NoRecordsFound(Exception):
    """
    Exception raised when no records are found in the database.

    This exception is intended to indicate that an attempted retrieval of data
    from the database has resulted in no records being found. It can include
    an additional message for context.
    """
    def __init__(self, message: str = "No additional message"):
        """
        Represents a custom exception that is raised when no records are found in the database.
        This exception accepts an optional message to provide additional information about the
        specific context or reason for the absence of records.

        :param message: A string providing additional context or information about the
            absence of records in the database. Defaults to "No additional message".
        """
        super().__init__(f"No records found on database ({message})")
