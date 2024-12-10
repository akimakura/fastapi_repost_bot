from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

# Токен вашего Telegram-бота и ID канала
BOT_TOKEN = "7993686607:AAHJUc8VbCPxzxpRDjkadqjbrwc1py2J0Jk"
CHANNEL_ID = "-1002366484212"


class Message(BaseModel):
    message: str


@app.post("/forward")
def forward_message(data: Message):
    """
    Получает сообщение от бота и пересылает его в Telegram канал.
    """
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": data.message
    }

    # Отправка сообщения в Telegram канал
    response = requests.post(telegram_url, json=payload)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Ошибка отправки сообщения в Telegram канал")

    return {"status": "success", "message": "Сообщение отправлено в канал"}
