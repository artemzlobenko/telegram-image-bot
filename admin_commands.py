from optparse import AmbiguousOptionError
from re import A
from telegram import InputMediaPhoto, KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.error import BadRequest
from telegram.ext import ContextTypes

from image import Image
from user import User
from config import ADMIN_TG_ID


async def stat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_user.id) == str(ADMIN_TG_ID):
        stat = await User.get_stat()
        if stat:
            stat_message = ''
                
            await context.bot.send_message(
                chat_id=type(stat) + '   ' + type[stat[0]] + type[stat[0][0]],
                text=stat_message,
            )
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='There are no users.',
            )
