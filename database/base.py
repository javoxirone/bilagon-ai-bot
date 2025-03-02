import os
import psycopg2
from psycopg2 import OperationalError, DataError

from exceptions.database import RollbackError, CommitError, DBError, DataTypeError


class Database:
    """
    Base class for repositories interacting with a database.
    """
    def __init__(self):
        """
        Initialize database connection.
        """
        self.db_name = os.getenv("DB_NAME")
        try:
            self.conn = psycopg2.connect(
                database=self.db_name,
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT")
            )
        except Exception as e:
            raise DBError(f"Failed to connect to database: {str(e)}")

    def commit(self):
        """
        Commit the current transaction.
        """
        try:
            if self.conn and not self.conn.closed:
                self.conn.commit()
        except Exception as e:
            self.rollback()
            raise CommitError(original_exception=e)

    def rollback(self):
        """
        Rollback the current transaction.
        """
        try:
            if self.conn and not self.conn.closed:
                self.conn.rollback()
        except Exception as e:
            raise RollbackError(original_exception=e)

    def close(self):
        """
        Close the database connection.
        """
        if self.conn and not self.conn.closed:
            self.conn.close()

    def execute_query(self, query, params=None):
        """
        Execute a query and return the cursor.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params or ())
            return cursor
        except OperationalError as e:
            self.rollback()
            raise DBError(f"Operational error: {str(e)}")
        except DataError as e:
            self.rollback()
            raise DataTypeError(f"Data type error: {str(e)}")
        except Exception as e:
            self.rollback()
            raise DBError(f"Database error: {str(e)}")