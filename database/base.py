import os
import psycopg2
from exceptions.database import RollbackError, CommitError


class Database:
    """
    Base class for repositories interacting with a database.

    This class provides a foundation for database interaction by managing the
    database connection. It uses environment variables for connection parameters
    and implements context management to ensure proper handling of database
    transactions. By utilizing this class, derived classes can focus on specific
    repository logic without worrying about connection and transaction management.

    :ivar db_name: Name of the database fetched from environment variables.
    :type db_name: str
    :ivar conn: Connection object to the database.
    :type conn: psycopg2.extensions.connection
    """
    def __init__(self):
        """
        Initialization of the base class for repositories to work with database.
        """
        self.db_name = os.getenv("DB_NAME")
        self.conn = psycopg2.connect(
            database=self.db_name,
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Handles the exit logic for a context manager dealing with database
        transactions. Ensures that transactions are correctly committed or
        rolled back depending on whether an exception occurred within the
        context. Additionally, guarantees the closing of the database
        connection after transaction handling.

        :param exc_type: The exception type if any exception was raised in the
                         with block, otherwise None.
        :param exc_val: The exception value if any exception was raised in the
                        with block, otherwise None.
        :param exc_tb: The traceback if any exception was raised in the with
                       block, otherwise None.
        :return: Always returns False to indicate that exceptions should not
                 be suppressed.
        """
        if exc_type is not None:
            try:
                self.conn.rollback()
            except Exception as rollback_error:
                raise RollbackError(original_exception=rollback_error)
            finally:
                self.conn.close()
        else:
            try:
                self.conn.commit()
            except Exception as commit_error:
                self.conn.rollback()
                raise CommitError(original_exception=commit_error)
            finally:
                self.conn.close()
        return False
