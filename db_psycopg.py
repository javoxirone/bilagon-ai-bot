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
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                telegram_id INTEGER UNIQUE,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                language TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                conversation_id SERIAL PRIMARY KEY,
                user_id INTEGER,
                role CHAR(15),
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
            )
        ''')
        self.conn.commit()

    def add_user(self, telegram_id, username, first_name, last_name, language):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO users (telegram_id, username, first_name, last_name, language)
            VALUES (%s, %s, %s, %s, %s)
        ''', (telegram_id, username, first_name, last_name, language))
        self.conn.commit()

    def get_user_by_telegram_id(self, telegram_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE telegram_id = %s', (telegram_id,))
        user_data = cursor.fetchone()
        print(user_data)

        if user_data:
            user_info = {
                "user_id": user_data[0],
                "telegram_id": user_data[1],
                "username": user_data[2],
                "first_name": user_data[3],
                "last_name": user_data[4],
                "created_at": user_data[5],
                "language": user_data[6]
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
                "created_at": user_data[5],
                "language": user_data[6]
            }
            user_info_list.append(user_info)

        return user_info_list

    def change_language(self, telegram_id, new_language):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE users SET language = %s WHERE telegram_id = %s',
                       (new_language, telegram_id))
        self.conn.commit()

    def user_exists(self, telegram_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users WHERE telegram_id = %s', (telegram_id,))
        count = cursor.fetchone()[0]
        return count > 0

    def add_conversation(self, telegram_id, role, message):
        # Get user_id for the given telegram_id
        user_info = self.get_user_by_telegram_id(telegram_id)

        if user_info:
            user_id = user_info["user_id"]
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO conversations (user_id, role, message)
                VALUES (%s, %s, %s)
            ''', (user_id, role, message))
            self.conn.commit()
        else:
            print(f"User with telegram_id {telegram_id} not found.")

    def reset_conversations(self, telegram_id):
        # Get user_id for the given telegram_id
        user_info = self.get_user_by_telegram_id(telegram_id)

        if user_info:
            user_id = user_info["user_id"]
            cursor = self.conn.cursor()
            cursor.execute('DELETE FROM conversations WHERE user_id = %s', (user_id,))
            self.conn.commit()
            print(f"All conversations for telegram_id {telegram_id} have been reset.")
        else:
            print(f"User with telegram_id {telegram_id} not found.")

    def get_conversations_by_telegram_id(self, telegram_id):
        # Get user_id for the given telegram_id
        user_info = self.get_user_by_telegram_id(telegram_id)

        if user_info:
            user_id = user_info["user_id"]
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT role, message FROM conversations
                WHERE user_id = %s
                ORDER BY created_at
            ''', (user_id,))
            conversations = cursor.fetchall()

            conversation_list = []
            for conversation_data in conversations:
                role, message = conversation_data
                conversation_info = {
                    "role": role.strip(),
                    "content": message.strip()
                }
                print(conversation_info)
                conversation_list.append(conversation_info)

            return conversation_list
        else:
            print(f"User with telegram_id {telegram_id} not found.")
            return None

    def close(self):
        self.conn.close()
