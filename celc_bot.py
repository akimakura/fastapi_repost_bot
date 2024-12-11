from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Update, BotCommand
from fastapi import FastAPI, Request
from pydantic import BaseModel
import asyncio

# Настройки
BOT_TOKEN = "7993686607:AAHJUc8VbCPxzxpRDjkadqjbrwc1py2J0Jk"
CHANNEL_ID = "-1002366484212"  # Или -100XXXXXXXXXX для приватного канала
WEBHOOK_PATH = f"/bot/{BOT_TOKEN}"  # Уникальный путь для вебхуков
WEBHOOK_URL = f"https://e778-95-25-236-76.ngrok-free.app{WEBHOOK_PATH}"  # Полный URL вебхука


# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Инициализация FastAPI
app = FastAPI()


# Модель для FastAPI запросов
class Message(BaseModel):
    message: str


# --- Обработчики Telegram-бота ---
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Привет! Отправь мне сообщение, и я пересылю его в канал!")


@dp.message()
async def handle_user_message(message: types.Message):
    """
    Обрабатывает текстовые сообщения от пользователей и пересылает их в канал.
    """
    try:
        await bot.send_message(CHANNEL_ID, f"Сообщение от {message.from_user.first_name}:\n{message.text}")
        await message.answer("Ваше сообщение отправлено в канал!")
    except Exception as e:
        await message.answer(f"Произошла ошибка при отправке: {e}")


# --- Эндпоинты FastAPI ---
@app.post(WEBHOOK_PATH)
async def telegram_webhook(update: dict):
    """
    Эндпоинт для обработки вебхуков от Telegram.
    """
    telegram_update = Update(**update)
    await dp.feed_update(bot, telegram_update)
    return {"status": "ok"}


@app.post("/forward")
async def forward_message(data: Message):
    """
    Эндпоинт для пересылки сообщений в Telegram канал через FastAPI.
    """
    try:
        await bot.send_message(CHANNEL_ID, data.message)
        return {"status": "success", "message": "Сообщение отправлено в канал"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


# --- События FastAPI ---
@app.on_event("startup")
async def on_startup():
    """
    Настройка вебхуков при запуске приложения.
    """
    # Устанавливаем команды бота
    await bot.set_my_commands([BotCommand(command="start", description="Начать")])
    # Устанавливаем вебхук
    await bot.set_webhook(WEBHOOK_URL)
    print(f"Вебхук установлен: {WEBHOOK_URL}")


@app.on_event("shutdown")
async def on_shutdown():
    """
    Очистка ресурсов при завершении работы приложения.
    """
    await bot.session.close()


# --- Запуск приложения ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
