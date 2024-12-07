import os
import psycopg2

from exceptions.database import RollbackError, CommitError


class Database:
    def __init__(self):
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
