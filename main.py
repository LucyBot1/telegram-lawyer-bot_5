# main.py
from aiogram import Bot, Dispatcher, types, executor
import asyncio
from fastapi import FastAPI
import uvicorn
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

app = FastAPI()

@app.get("/")
def root():
    return {"status": "bot is running"}

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer("Привет! Я юридический бот.")

async def start_bot():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling()

loop = asyncio.get_event_loop()
loop.create_task(start_bot())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
