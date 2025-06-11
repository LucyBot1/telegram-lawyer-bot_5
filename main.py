import os
import asyncio
from aiogram import Bot, Dispatcher, types
from fastapi import FastAPI
import uvicorn

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Bot is running"}

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer("Привет! Я юридический бот.")

async def start_bot():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling()

# Создаём задачу запуска бота параллельно с веб-сервером
@app.on_event("startup")
async def on_startup():
    @dp.message_handler()
async def text_handler(message: types.Message):
    text = message.text.lower()

    if "что ты умеешь" in text:
        await message.answer("Я могу отвечать на юридические вопросы и помогать с созданием документов.")
    else:
        await message.answer("Пожалуйста, уточни свой юридический вопрос.")
    asyncio.create_task(start_bot())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
