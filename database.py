from dataclasses import dataclass
from settings import DB_PATH
import sqlite3



@dataclass
class User:
    tg_id: int
    first_name: str = ''
    last_name: str = ''
    username: str = ''
           
    async def set_user(self) -> None:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute('''
                    INSERT OR REPLACE INTO user (tg_id, name, surname, username)
                    VALUES (?, ?, ?, ?)
                    ''', (self.tg_id, self.first_name, self.last_name, self.username))
        conn.commit()
        conn.close()
        
    def get_unwatched_image_ids(tg_id):
        pass
