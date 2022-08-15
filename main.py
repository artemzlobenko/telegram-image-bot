from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler
from telegram.ext.filters import Text

from image import Image
from bot_commands import start, images
from bot_commands import GET_IMAGES_TEXT
from config import BOT_TOKEN, CSV_PATH


def main():
    Image.update_images(CSV_PATH)
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    start_handler = CommandHandler('start', start)
    images_handler = MessageHandler(Text(GET_IMAGES_TEXT), images)
    application.add_handler(start_handler)
    application.add_handler(images_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
