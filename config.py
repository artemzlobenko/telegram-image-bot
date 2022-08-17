import os
import logging


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')
DB_URI = os.getenv('DB_URI')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
APP_URL = os.getenv('APP_URL')

# Path to CSV files. Files have to contain one link per row. The file's name
# will be used as the theme of an image.
CSV_PATH = os.getenv('CSV_PATH')
