import csv 
import glob
import sqlite3
import os
from pathlib import Path
from dataclasses import dataclass

from validators import url

from config import DB_URI


@dataclass
class Image:
    id: int
    url: str
    theme: str
    
    @classmethod
    async def get_unwatched_images(cls, user_id: int, number_of_images: int = 10) -> list:
        conn = sqlite3.connect(DB_URI)
        cur = conn.cursor()
        image_list = cur.execute('''
                    SELECT *
                    FROM image
                    WHERE id NOT IN (
                        SELECT image_id
                        FROM watched_images
                        WHERE user_id = ?
                    )
                    LIMIT ?
                    ''', (user_id, number_of_images)).fetchall()
        conn.close()
        images = [Image(*image_dict) for image_dict in image_list]
        return images
    
    @classmethod
    async def update_watched_images(cls, tg_id: int, images: list) -> None:
        conn = sqlite3.connect(DB_URI)
        cur = conn.cursor()
        for image in images:
            cur.execute('''
                        INSERT INTO watched_images (user_id, image_id)
                        VALUES (?, ?)
                        ON CONFLICT DO NOTHING
                        ''', (tg_id, image.id))
            conn.commit()
        conn.close()

    @classmethod
    def update_images(cls, csv_path) -> None:
        """
        Insert themes and URLs of images from CSV files into the database.
        """
        file_path_iter = glob.iglob(os.path.join(csv_path, '*.csv'))
        for file_path in file_path_iter:
            with open(file_path) as url_file:
                url_reader = csv.reader(url_file)
                for image_url in url_reader:
                    if url(image_url[0]):
                        theme = Path(file_path).stem
                        Image.set_image(image_url[0], theme)

    @classmethod
    def set_image(cls, url, theme) -> None:
        conn = sqlite3.connect(DB_URI)
        cur = conn.cursor()
        cur.execute('''
                    INSERT INTO image (url, theme)
                    VALUES (?, ?)
                    ON CONFLICT DO NOTHING
                    ''', (url, theme))
        conn.commit()
        conn.close()
