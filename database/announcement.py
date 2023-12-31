from psycopg2.extras import DictCursor

from .base import Database


class Announcement(Database):
    def __init__(self, db_name=None):
        super().__init__(db_name)

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS announcements (
                announcement_id SERIAL PRIMARY KEY,
                telegram_id INTEGER REFERENCES users(telegram_id),
                telegram_message_id INTEGER,
                is_ad BOOLEAN DEFAULT false,
                image_url VARCHAR(255),
                content TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        self.conn.commit()

    def create_announcement(self, telegram_id, telegram_message_id, is_ad=False, image_url=None, content=None):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO announcements (telegram_id, telegram_message_id, is_ad, image_url, content)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING announcement_id;
        ''', (telegram_id, telegram_message_id, is_ad, image_url, content))
        announcement_id = cursor.fetchone()[0]
        self.conn.commit()
        return announcement_id

    def get_announcements(self):
        cursor = self.conn.cursor(cursor_factory=DictCursor)
        cursor.execute('SELECT * FROM announcements;')
        raw_data = cursor.fetchall()
        data = []
        for item in raw_data:
            payload = {
                "id": item[0],
                "telegram_id": item[1],
                "telegram_message_id": item[2],
                "is_ad": item[3],
                "image_url": item[4],
                "content": item[5],
                "created_at": item[6],
                "updated_at": item[7],
            }
            data.append(payload)
        return data

    def get_announcement(self, announcement_id):
        cursor = self.conn.cursor(cursor_factory=DictCursor)
        cursor.execute('SELECT * FROM announcements WHERE announcement_id = %s;', (announcement_id,))
        item = cursor.fetchone()
        payload = {
            "id": item[0],
            "telegram_id": item[1],
            "telegram_message_id": item[2],
            "is_ad": item[3],
            "image_url": item[4],
            "content": item[5],
            "created_at": item[6],
            "updated_at": item[7],
        }
        return payload

    def update_announcement(self, announcement_id, is_ad=None, image_url=None, content=None):
        cursor = self.conn.cursor()
        update_query = 'UPDATE announcements SET updated_at = CURRENT_TIMESTAMP'
        if is_ad is not None:
            update_query += ', is_ad = %s'
        if image_url is not None:
            update_query += ', image_url = %s'
        if content is not None:
            update_query += ', content = %s'
        update_query += ' WHERE announcement_id = %s;'
        cursor.execute(update_query, (is_ad, image_url, content, announcement_id))
        self.conn.commit()

    def delete_announcement(self, announcement_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM announcements WHERE announcement_id = %s;', (announcement_id,))
        self.conn.commit()

    def close(self):
        if self.conn is not None:
            self.conn.close()
