from telegram import InputMediaPhoto, Update
from telegram.error import BadRequest
from telegram.ext import ContextTypes

from image import Image
from user import User


async def add_user(update: Update):
    await User.set_user(
        update.effective_user.id,
        update.effective_user.first_name,
        update.effective_user.last_name,
        update.effective_user.username,
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await add_user(update)
    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Hello, I\'m a bot! Press /images to get 10 images.'
    )

async def images(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await User.get_user(update.effective_user.id)
    if not user:
        await add_user(update)
        user = await User.get_user(update.effective_user.id)
    try:
        images = await Image.get_unwatched_images(user.id)
        media_photos = [InputMediaPhoto(media=image.url) for image in images]
        await context.bot.sendMediaGroup(
            chat_id = update.effective_chat.id,
            media = media_photos
        )
        
        await Image.update_watched_images(user.id, images)
    except BadRequest as e:
        print(e)
        await context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = 'There is no more content left :(' + '\n' +
                'But don\'t be upset, we add new beautiful images every week!' + '\n' +
                'Have a nice day!'
        )
