import os


from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler
from telegram.ext.filters import Text

from image import Image
from bot_commands import start, images
from bot_commands import GET_IMAGES_TEXT
from config import BOT_TOKEN, CSV_PATH, APP_URL


def main():
    PORT = int(os.environ.get('PORT', '5000'))
    Image.update_images(CSV_PATH)
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    start_handler = CommandHandler('start', start)
    #images_handler = MessageHandler(Text(GET_IMAGES_TEXT), images)
    application.add_handler(start_handler)
    #application.add_handler(images_handler)
    application.run_webhook(
        port=PORT,
        url_path=APP_URL
    )


if __name__ == '__main__':
    main()
