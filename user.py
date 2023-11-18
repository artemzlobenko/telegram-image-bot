from mysql import connector
from dataclasses import dataclass

from config import DB_PASSWORD, DB_URI, DB_USER, DB_NAME


@dataclass
class User:
    id: int
    tg_id: int
    first_name: str = ''
    last_name: str = ''
    username: str = ''

    @classmethod
    async def get_user(cls, tg_id: int):
        conn = connector.connect(host=DB_URI, database=DB_NAME, user=DB_USER,
                                password=DB_PASSWORD)
        cur = conn.cursor()
        cur.execute('''
                    SELECT *
                    FROM users
                    WHERE tg_id = %s
                    ''', (tg_id,))
        user_tuple = cur.fetchone()
        conn.close()
        return User(*user_tuple) if user_tuple else None

    @classmethod
    async def set_user(cls, tg_id: int, first_name: str,
                       last_name: str, username: str) -> None:

        conn = connector.connect(host=DB_URI, database=DB_NAME, user=DB_USER,
                                password=DB_PASSWORD)
        cur = conn.cursor()
        cur.execute('''
                    INSERT INTO users (tg_id, first_name, last_name, username)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE tg_id=tg_id
                    ''', (tg_id, first_name, last_name, username))
        conn.commit()
        conn.close()

    @classmethod
    async def get_stat(cls) -> tuple:
        conn = connector.connect(host=DB_URI, database=DB_NAME, user=DB_USER,
                                password=DB_PASSWORD)
        cur = conn.cursor()
        cur.execute('''
                    SELECT first_name, COUNT(*) as watched_images
                    FROM users
                    JOIN watched_images ON watched_images.user_id = users.id
                    GROUP by first_name
                    ''')
        user_info_tuple = cur.fetchall()
        conn.close()
        return user_info_tuple

    async def update_user(self, tg_id: int, first_name: str = None,
                       last_name: str = None, username: str = None) -> None:

        conn = connector.connect(host=DB_URI, database=DB_NAME, user=DB_USER,
                                password=DB_PASSWORD)
        cur = conn.cursor()
        cur.execute('''
                    UPDATE users
                    SET first_name = %s,
                        last_name = %s,
                        username = %s
                    WHERE tg_id = %s
                    ''', (first_name, last_name, username, tg_id))
        conn.commit()
        conn.close()
