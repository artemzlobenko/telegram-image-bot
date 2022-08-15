import sqlite3
from dataclasses import dataclass

from config import DB_PATH


@dataclass
class User:
    id: int
    tg_id: int
    first_name: str = ''
    last_name: str = ''
    username: str = ''

    @classmethod
    async def get_user(cls, tg_id: int):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        user_tuple = cur.execute('''
                    SELECT *
                    FROM user
                    WHERE tg_id = ?
                    ''', (tg_id,)).fetchone()
        conn.close()
        return User(*user_tuple) if user_tuple else None
    
    @classmethod
    async def set_user(cls, tg_id: int, first_name: str, 
                       last_name: str, username: str) -> None:
        
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute('''
                    INSERT INTO user (tg_id, name, surname, username)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT (tg_id) DO UPDATE
                    SET name = ?,
                        surname = ?,
                        username = ?
                    ''', (tg_id, first_name, last_name, username,
                          first_name, last_name, username))
        conn.commit()
        conn.close()
