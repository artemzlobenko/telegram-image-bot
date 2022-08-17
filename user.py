import psycopg2
from dataclasses import dataclass

from config import DB_PASSWORD, DB_URI, DB_USER


@dataclass
class User:
    id: int
    tg_id: int
    first_name: str = ''
    last_name: str = ''
    username: str = ''

    @classmethod
    async def get_user(cls, tg_id: int):
        conn = psycopg2.connect(dbname=DB_URI, user=DB_USER,
                                password=DB_PASSWORD)
        cur = conn.cursor()
        cur.execute('''
                    SELECT *
                    FROM users
                    WHERE tg_id = ?
                    ''', (tg_id,))
        user_tuple = cur.fetchone()
        conn.close()
        return User(*user_tuple) if user_tuple else None
    
    @classmethod
    async def set_user(cls, tg_id: int, first_name: str, 
                       last_name: str, username: str) -> None:
        
        conn = psycopg2.connect(dbname=DB_URI, user=DB_USER,
                                password=DB_PASSWORD)
        cur = conn.cursor()
        cur.execute('''
                    INSERT INTO users (tg_id, name, surname, username)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT (tg_id) DO UPDATE
                    SET name = ?,
                        surname = ?,
                        username = ?
                    ''', (tg_id, first_name, last_name, username,
                          first_name, last_name, username))
        conn.commit()
        conn.close()
