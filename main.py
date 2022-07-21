from database import User
from settings import BOT_TOKEN
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_id = update.effective_user.id
    first_name = update.effective_user.first_name
    last_name = update.effective_user.last_name
    username = update.effective_user.username
    user = User(tg_id, first_name, last_name, username)
    await user.set_user()
    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = "Hello, I'm a bot! Press images to get 10 images."
    )
    

def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
