from .base import Database
from .user import User


class Conversation(Database):
    def __init__(self, db_name=None):
        super().__init__(db_name)

    def create_table(self):
        cursor = self.conn.cursor()
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

    def add_conversation(self, telegram_id, role, message):
        # Get user_id for the given telegram_id
        user_db = User()
        user_info = user_db.get_user_by_telegram_id(telegram_id)
        user_db.close()

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
        user_db = User()
        user_info = user_db.get_user_by_telegram_id(telegram_id)
        user_db.close()
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
        user_db = User()
        user_info = user_db.get_user_by_telegram_id(telegram_id)
        user_db.close()

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
