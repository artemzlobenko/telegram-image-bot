from telegram import Update
from telegram.ext import ContextTypes
import urllib

from user import User
from image import Image
from config import ADMIN_TG_ID


async def stat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_user.id) == str(ADMIN_TG_ID):
        stat = await User.get_stat()
        if stat:
            stat_message = ''
            for data in stat:
                stat_message += ' | '.join(map(str, data)) + '\n'
                
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=stat_message,
            )
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='There are no users.',
            )

async def add_images(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_user.id) == str(ADMIN_TG_ID):
        file_id = update.effective_message.document.file_id
        csv_file = await context.bot.get_file(file_id)
        csv_file.download()
        
        csv_bytestream = csv_file.file_path
        file_name = update.effective_message.document.file_name
        image_theme = file_name.replace('.csv', '')
        await Image.update_images(csv_bytestream, image_theme)
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='New images have been added to the database.',
            )
