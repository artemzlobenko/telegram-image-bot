import csv 
import glob
import psycopg2
import os
from pathlib import Path
from dataclasses import dataclass

from validators import url

from config import DB_NAME, DB_PASSWORD, DB_URI, DB_USER


@dataclass
class Image:
    id: int
    url: str
    theme: str
    
    @classmethod
    async def get_unwatched_images(cls, user_id: int, number_of_images: int = 10) -> list:
        conn = psycopg2.connect(DB_URI, dbname=DB_NAME, user=DB_USER,
                                password=DB_PASSWORD)
        cur = conn.cursor()
        cur.execute('''
                SELECT *
                FROM images
                WHERE id NOT IN (
                    SELECT image_id
                    FROM watched_images
                    WHERE user_id = %s
                )
                LIMIT %s
                ''', (user_id, number_of_images))
        image_list = cur.fetchall()
        conn.close()
        images = [Image(*image_dict) for image_dict in image_list]
        return images
    
    @classmethod
    async def update_watched_images(cls, tg_id: int, images: list) -> None:
        conn = psycopg2.connect(DB_URI, dbname=DB_NAME, user=DB_USER,
                                password=DB_PASSWORD)
        cur = conn.cursor()
        for image in images:
            cur.execute('''
                        INSERT INTO watched_images (user_id, image_id)
                        VALUES (%s, %s)
                        ''', (tg_id, image.id))
            conn.commit()
        conn.close()

    @classmethod
    async def update_images(cls, csv_file) -> None:
        """
        Insert themes and URLs of images from CSV file into the database.
        """
        with open(csv_file) as url_file:
            url_reader = csv.reader(url_file)
            for image_url in url_reader:
                if url(image_url[0]) and not Image.get_image(image_url[0]):
                    theme = Path(csv_file).stem
                    Image.set_image(image_url[0], theme)

    @classmethod
    def set_image(cls, url, theme) -> None:
        conn = psycopg2.connect(DB_URI, dbname=DB_NAME, user=DB_USER,
                                password=DB_PASSWORD)
        cur = conn.cursor()
        cur.execute('''
                    INSERT INTO images (url, theme)
                    VALUES (%s, %s)
                    ON CONFLICT (url) DO NOTHING
                    ''', (url, theme))
        conn.commit()
        conn.close()

    @classmethod
    def get_image(cls, url) -> None:
        conn = psycopg2.connect(DB_URI, dbname=DB_NAME, user=DB_USER,
                                password=DB_PASSWORD)
        cur = conn.cursor()
        cur.execute('''
                    SELECT * FROM images
                    WHERE url = %s
                    ''', (url,))
        image = cur.fetchone()
        conn.close()
        return Image(*image) if image else None
