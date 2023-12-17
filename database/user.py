from .base import Database


class User(Database):
    def __init__(self, db_name=None):
        super().__init__(db_name)

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
