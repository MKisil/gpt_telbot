import asyncio

from aiogram import Dispatcher
from dotenv import find_dotenv, load_dotenv

from bot.bot_client import bot
from handlers.user_group import user_group_router

load_dotenv(find_dotenv())

ALLOWED_UPDATES = ['message']

dp = Dispatcher()

dp.include_router(user_group_router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


asyncio.run(main())
