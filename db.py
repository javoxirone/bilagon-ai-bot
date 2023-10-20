import sqlite3
from datetime import datetime, timedelta



class UserDatabase:
    def __init__(self, db_name=None):
        self.db_name = db_name or "user_db.sqlite"
        self.conn = sqlite3.connect(self.db_name)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                telegram_id INTEGER UNIQUE,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                has_premium_gpt3 BOOLEAN,
                has_premium_gpt4 BOOLEAN,
                gpt3_requests_num INTEGER,
                gpt4_token INTEGER,
                language TEXT,
                gpt3_requests_expire_datetime DATETIME,
                gpt3_premium_purchase_datetime DATETIME
            )
        ''')
        self.conn.commit()

    def add_user(self, telegram_id, username, first_name, last_name, language):
        cursor = self.conn.cursor()
        now = datetime.now()
        expire_datetime = now + timedelta(hours=24)
        cursor.execute('''
            INSERT INTO users (telegram_id, username, first_name, last_name, 
                has_premium_gpt3, has_premium_gpt4, gpt3_requests_num, gpt4_token, language, gpt3_requests_expire_datetime, gpt3_premium_purchase_datetime)
            VALUES (?, ?, ?, ?, 0, 0, 5, 0, ?, ?, NULL)
        ''', (telegram_id, username, first_name, last_name, language, expire_datetime))
        self.conn.commit()

    def get_user_by_telegram_id(self, telegram_id):
        from utils import format_datetime

        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,))
        user_data = cursor.fetchone()

        if user_data:
            user_info = {
                "telegram_id": user_data[1],
                "username": user_data[2],
                "first_name": user_data[3],
                "last_name": user_data[4],
                "has_premium_gpt3": bool(user_data[5]),
                "has_premium_gpt4": bool(user_data[6]),
                "gpt3_requests_num": user_data[7],
                "gpt4_token": user_data[8],
                "language": user_data[9],
                "gpt3_requests_expire_datetime": format_datetime(user_data[10]),
                "gpt3_premium_purchase_datetime": format_datetime(user_data[11]),
            }
            return user_info
        else:
            return None

    def get_all_users(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()

        user_info_list = []
        for user_data in users:
            user_info = {
                "telegram_id": user_data[1],
                "username": user_data[2],
                "first_name": user_data[3],
                "last_name": user_data[4],
                "has_premium_gpt3": bool(user_data[5]),
                "has_premium_gpt4": bool(user_data[6]),
                "gpt3_requests_num": user_data[7],
                "gpt4_token": user_data[8],
                "language": user_data[9]
            }
            user_info_list.append(user_info)

        return user_info_list

    def change_language(self, telegram_id, new_language):
        # Change the language for a user.
        cursor = self.conn.cursor()
        cursor.execute('UPDATE users SET language = :new_language WHERE telegram_id = :telegram_id',
                       {'new_language': new_language, 'telegram_id': telegram_id})
        self.conn.commit()

    def update_subscription(self, telegram_id, subscription_type, token=None):
        # Update a user's subscription and token.
        cursor = self.conn.cursor()
        if subscription_type == "premium_gpt3":
            cursor.execute('UPDATE users SET has_premium_gpt3 = 1, gpt3_requests_num = ? WHERE telegram_id = ?',
                           (token, telegram_id))
        elif subscription_type == "premium_gpt4":
            cursor.execute('UPDATE users SET has_premium_gpt4 = 1, gpt4_token = ? WHERE telegram_id = ?',
                           (token, telegram_id))
        self.conn.commit()

    def update_tokens(self, telegram_id, model, tokens):
        cursor = self.conn.cursor()
        if model == "gpt3":
            cursor.execute('UPDATE users SET gpt3_requests_num = ? WHERE telegram_id = ?', (tokens, telegram_id))
        elif model == "gpt4":
            cursor.execute('UPDATE users SET gpt4_token = ? WHERE telegram_id = ?', (tokens, telegram_id))
        self.conn.commit()

    def user_exists(self, telegram_id):
        # Check if a user with a given Telegram ID exists in the database.
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users WHERE telegram_id = ?', (telegram_id,))
        count = cursor.fetchone()[0]
        return count > 0

    def has_premium_subscription(self, telegram_id, model):
        cursor = self.conn.cursor()
        if model == "gpt3":
            cursor.execute('SELECT has_premium_gpt3 FROM users WHERE telegram_id = ?', (telegram_id,))
        elif model == "gpt4":
            cursor.execute('SELECT has_premium_gpt4 FROM users WHERE telegram_id = ?', (telegram_id,))
        result = cursor.fetchone()
        if result:
            return bool(result[0])
        return False

    def set_gpt3_requests_expire_datetime(self, telegram_id, expire_datetime):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE users SET gpt3_requests_expire_datetime = ? WHERE telegram_id = ?',
                       (expire_datetime, telegram_id))
        self.conn.commit()

    def set_gpt3_premium_purchase_datetime(self, telegram_id, purchase_datetime):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE users SET gpt3_premium_purchase_datetime = ? WHERE telegram_id = ?',
                       (purchase_datetime, telegram_id))
        self.conn.commit()


    def close(self):
        # Close the database connection.
        self.conn.close()