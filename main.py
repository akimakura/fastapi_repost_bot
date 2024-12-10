
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests

# URL вашего FastAPI сервера
FASTAPI_URL = "http://127.0.0.1:8000/forward"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь мне сообщение, и я передам его на сервер!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text

    # Отправляем сообщение на FastAPI сервер
    response = requests.post(FASTAPI_URL, json={"message": message_text})
    if response.status_code == 200:
        await update.message.reply_text("Сообщение успешно отправлено на сервер!")
    else:
        await update.message.reply_text("Ошибка отправки сообщения на сервер!")



if __name__ == '__main__':
    application = ApplicationBuilder().token("7993686607:AAHJUc8VbCPxzxpRDjkadqjbrwc1py2J0Jk").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Telegram бот запущен!")
    application.run_polling()
