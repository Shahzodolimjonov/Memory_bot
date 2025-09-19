import asyncio
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz

import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID", "-1002381989382"))
DEFAULT_MESSAGE = os.getenv("DEFAULT_MESSAGE", "DEFAULT MESSAGE")

router = Router()
scheduler = AsyncIOScheduler()


async def send_message(bot: Bot):
    await bot.send_message(GROUP_ID, DEFAULT_MESSAGE)


@router.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Bot ishga tushdi")


async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    tz = pytz.timezone("Asia/Tashkent")
    # scheduler.add_job(send_message, "cron", hour=23, minute=42, timezone=tz, args=[bot])
    # scheduler.add_job(send_message, "cron", hour=23, minute=46, timezone=tz, args=[bot])
    scheduler.add_job(
        send_message,
        "cron",
        day_of_week="mon-fri",
        hour=10,
        minute=0,
        timezone=tz,
        args=[bot]
    )
    scheduler.add_job(
        send_message,
        "cron",
        day_of_week="mon-fri",
        hour=15,
        minute=30,
        timezone=tz,
        args=[bot]
    )
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to‘xtatildi")
