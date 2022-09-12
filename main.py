import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler
from telegram.ext.filters import Text

from image import Image
from bot_commands import start, images
from admin_commands import stat
from bot_commands import GET_IMAGES_TEXT
from config import BOT_TOKEN, CSV_PATH


def main():
    # Enable logging
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO
    )
    
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    start_handler = CommandHandler('start', start)
    images_handler = MessageHandler(Text(GET_IMAGES_TEXT), images)
    admin_stat_handler = CommandHandler('stat', stat)
    application.add_handler(admin_stat_handler)
    application.add_handler(start_handler)
    application.add_handler(images_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
