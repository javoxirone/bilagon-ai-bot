import os
import psycopg2


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
            print(f"An exception occurred: {exc_type}, {exc_val}, {exc_tb}")
        self.conn.close()
        return False