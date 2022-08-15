import os


BOT_TOKEN = os.getenv('BOT_TOKEN')
DB_PATH = os.getenv('DB_PATH')

# Path to CSV files. Files have to contain one link per row. The file's name
# will be used as the theme of an image.
CSV_PATH = os.getenv('CSV_PATH')
