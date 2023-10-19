"""
This is a echo bot.
It echoes any incoming text messages.
"""
import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.utils import executor

from config import API_TOKEN

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

from app import *

# Configure logging
logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
