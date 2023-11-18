import os
from dotenv import load_dotenv


project_folder = os.path.expanduser('~/telegram-image-bot/')
load_dotenv(os.path.join(project_folder, '.env'))

ADMIN_TG_ID = os.getenv('ADMIN_TG_ID')
BOT_TOKEN = os.getenv('BOT_TOKEN')
DB_URI = os.getenv('DATABASE_URL')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

# Path to CSV files. Files have to contain one link per row. The file's name
# will be used as the theme of an image.
CSV_PATH = os.getenv('CSV_PATH')
