import logging
import os
import sqlite3

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

with sqlite3.connect("db.sqlite3") as cursor:
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            full_name TEXT NOT NULL,
            position TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            website TEXT NOT NULL
            )
        """
    )


async def set_default_commands():
    await dp.bot.set_my_commands(
        [
            types.BotCommand("cancel", "Отмена"),
            types.BotCommand("register", "Регистрация"),
            types.BotCommand("createoffer", "Создать КП"),
            types.BotCommand("editprofile", "Редактировать профиль"),
        ]
    )
