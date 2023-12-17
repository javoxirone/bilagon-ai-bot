import os
import psycopg2


class Database:
    def __init__(self, db_name=None):
        self.db_name = db_name or os.getenv("DB_NAME")
        self.conn = psycopg2.connect(
            database=self.db_name,
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )

    def close(self):
        self.conn.close()
