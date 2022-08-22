from telegram import InputMediaPhoto, KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.error import BadRequest
from telegram.ext import ContextTypes

from image import Image
from user import User


GET_IMAGES_TEXT = 'Get images 🎋'


async def add_user(update: Update):
    await User.set_user(
        update.effective_user.id,
        first_name=update.effective_user.first_name,
        last_name=update.effective_user.last_name,
        username=update.effective_user.username
    )

async def update_user(update: Update):
    await User.update_user(
        update.effective_user.first_name,
        update.effective_user.last_name,
        update.effective_user.username,
        update.effective_user.id
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    buttons = [[KeyboardButton(GET_IMAGES_TEXT)]]
    
    if not await User.get_user(update.effective_user.id):
        await add_user(update)
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Hello, I\'m need_for_picture bot! ' +
            'Press Get images 🎋 to get 10 images.',
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )

async def images(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    user = await User.get_user(update.effective_user.id)
    if not user:
        await add_user(update)
        user = await User.get_user(update.effective_user.id)
    else:
        await update_user(update)
        
    try:
        images = await Image.get_unwatched_images(user.id)
        media_photos = [InputMediaPhoto(media=image.url) for image in images]
        await context.bot.sendMediaGroup(
            chat_id=update.effective_chat.id,
            media=media_photos
        )
        
        await Image.update_watched_images(user.id, images)
        
    except BadRequest as e:
        print(e)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='There is no more content left :(' + '\n' +
                'But i\'ts okay, we add new pictures every week!' + '\n' +
                'Have a nice day!'
        )
