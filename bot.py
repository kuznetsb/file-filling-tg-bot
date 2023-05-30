import sqlite3

from aiogram import executor, types
from aiogram.dispatcher import FSMContext

from config import dp
from handlers.offer import handle_offer_creation
from handlers.users import (
    handle_user_creation,
    handle_editing_user_profile,
    handle_change_permission,
)
from handlers.template import handle_template_edit


async def set_default_commands(dispatcher):
    await dispatcher.bot.set_my_commands(
        [
            types.BotCommand("cancel", "Отмена"),
            types.BotCommand("register", "Регистрация"),
            types.BotCommand("create_offer", "Создать КП"),
            types.BotCommand("edit_template", "Редактировать инфо для шаблона"),
            types.BotCommand("edit_profile", "Редактировать профиль"),
        ]
    )


@dp.message_handler(commands=["create_offer"])
async def create_offer(message: types.Message):
    with sqlite3.connect("db.sqlite3") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id=?", (message.from_user.id,))
        user = cursor.fetchone()
    if user:
        await handle_offer_creation(message)
    else:
        await message.answer(
            "Для создания КП сначала заполните свои данные -> /register"
        )


@dp.message_handler(commands=["register"])
async def create_profile(message: types.Message):
    await handle_user_creation(message)


@dp.message_handler(commands=["edit_profile"])
async def edit_profile(message: types.Message):
    await handle_editing_user_profile(message)


@dp.message_handler(commands=["edit_template"])
async def cancel_state(message: types.Message):
    await handle_template_edit(message)


@dp.message_handler(commands=["permission"])
async def cancel_state(message: types.Message):
    await handle_change_permission(message)


@dp.message_handler(commands=["cancel"], state="*")
async def cancel_state(message: types.Message, state: FSMContext):
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=set_default_commands)
