import os

from aiogram import Bot
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
