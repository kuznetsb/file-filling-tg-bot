import sqlite3

from aiogram import executor, types
from aiogram.dispatcher import FSMContext

from config import dp
from handlers.invoice import handle_invoice_creation, add_specification_invoice
from handlers.offer import handle_offer_creation, add_specification_offer
from handlers.products import CreateProduct
from handlers.users import (
    handle_user_creation,
    handle_editing_user_profile,
    handle_change_permission,
)
from handlers.template import handle_template_edit
from keyboards.offer_keyboard import ADD_SPEC


async def set_default_commands(dispatcher):
    await dispatcher.bot.set_my_commands(
        [
            types.BotCommand("cancel", "Отмена"),
            types.BotCommand("register", "Регистрация"),
            types.BotCommand("create_offer", "Создать КП"),
            types.BotCommand("create_invoice", "Создать Счет"),
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


@dp.message_handler(commands=["create_invoice"])
async def create_invoice(message: types.Message):
    await handle_invoice_creation(message)


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


@dp.callback_query_handler(
    ADD_SPEC.filter(), state=CreateProduct.waiting_for_create_product
)
async def add_specification(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    data = await state.get_data()
    document = data["document"]
    if document == "invoice":
        await add_specification_invoice(call, callback_data, state)
    elif document == "offer":
        await add_specification_offer(call, callback_data, state)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=set_default_commands)
