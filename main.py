from telegram.ext import ApplicationBuilder, CommandHandler

from image import Image
from bot_commands import start, images
from config import BOT_TOKEN, CSV_PATH


def main():
    Image.update_images(CSV_PATH)
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    start_handler = CommandHandler('start', start)
    images_handler = CommandHandler('images', images)
    application.add_handler(start_handler)
    application.add_handler(images_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
