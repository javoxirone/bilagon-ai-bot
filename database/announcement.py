from .base import Database


class Announcement(Database):
    def __init__(self, db_name=None):
        super().__init__(db_name)

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS announcement (
                announcement_id SERIAL PRIMARY KEY,
                users INTEGER REFERENCES users(user_id),
                is_ad BOOLEAN DEFAULT false,
                image_url VARCHAR(255),
                content TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def create_announcement(self, users, is_ad, image_url, content):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO announcement (users, is_ad, image_url, content)
            VALUES (%s, %s, %s, %s)
            RETURNING announcement_id
        ''', (users, is_ad, image_url, content))
        self.conn.commit()
        return cursor.fetchone()[0]

    def get_announcement(self, announcement_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM announcement WHERE announcement_id = %s
        ''', (announcement_id,))
        return cursor.fetchone()

    def get_announcement_list(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM announcement
        ''')
        return cursor.fetchall()

    def update_announcement(self, announcement_id, users=None, is_ad=None, image_url=None, content=None):
        cursor = self.conn.cursor()
        update_query = 'UPDATE announcement SET '
        update_values = []
        if users is not None:
            update_query += 'users = %s, '
            update_values.append(users)
        if is_ad is not None:
            update_query += 'is_ad = %s, '
            update_values.append(is_ad)
        if image_url is not None:
            update_query += 'image_url = %s, '
            update_values.append(image_url)
        if content is not None:
            update_query += 'content = %s, '
            update_values.append(content)
        update_query = update_query.rstrip(', ') + ' WHERE announcement_id = %s'
        update_values.append(announcement_id)
        cursor.execute(update_query, update_values)
        self.conn.commit()

    def delete_announcement(self, announcement_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            DELETE FROM announcement WHERE announcement_id = %s
        ''', (announcement_id,))
        self.conn.commit()


