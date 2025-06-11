import os
import asyncio
from aiogram import Bot, Dispatcher, types
from fastapi import FastAPI
import uvicorn

# Получение токена из переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# FastAPI-приложение — нужно для Render (он требует открытый порт)
app = FastAPI()

@app.get("/")
def root():
    return {"status": "Bot is running"}

# Обработчик команды /start
@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer("Привет! Я юридический бот. Задайте свой вопрос.")

# Обработчик всех текстовых сообщений
@dp.message_handler()
async def handle_text(message: types.Message):
    text = message.text.lower()

    if "что ты умеешь" in text:
        await message.answer("Я могу отвечать на юридические вопросы по российскому законодательству и помогать с составлением документов.")
    else:
        await message.answer("Пожалуйста, уточните ваш юридический вопрос. Я постараюсь помочь.")

# Запуск polling параллельно с сервером FastAPI
@app.on_event("startup")
async def on_startup():
    asyncio.create_task(start_bot())

async def start_bot():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling()

# Запуск uvicorn-сервера (открывает порт для Render)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
