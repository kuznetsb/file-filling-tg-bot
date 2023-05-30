import sqlite3

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from config import dp
from keyboards.user_keyboard import (
    create_user_edit_keyboard,
    EDIT_FIELD,
    create_access_edit_keyboard,
)


class CreateUser(StatesGroup):
    waiting_for_full_name = State()
    waiting_for_position = State()
    waiting_for_phone = State()
    waiting_for_email = State()
    waiting_for_website = State()


class EditProfile(StatesGroup):
    waiting_what_to_edit = State()
    waiting_new = State()


class EditAccess(StatesGroup):
    waiting_type_of_editing = State()
    waiting_user_id = State()


async def handle_user_creation(message: types.Message):
    with sqlite3.connect("db.sqlite3") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id=?", (message.from_user.id,))
        user = cursor.fetchone()

    if user:
        await message.answer("Ты уже зарегистрирован, для изменения -> /edit_profile")
        return

    await CreateUser.waiting_for_full_name.set()
    await message.answer("ФИО")


@dp.message_handler(state=CreateUser.waiting_for_full_name)
async def get_user_name(message: types.Message, state: FSMContext):
    if message.text == "/cancel":
        await state.finish()
        return

    await state.update_data(full_name=message.text)

    await CreateUser.next()

    await message.answer("Введи свою должность")


@dp.message_handler(state=CreateUser.waiting_for_position)
async def get_user_position(message: types.Message, state: FSMContext):
    if message.text == "/cancel":
        await state.finish()
        return

    await state.update_data(position=message.text)

    await CreateUser.next()

    await message.answer("Введи номер телефона")


@dp.message_handler(state=CreateUser.waiting_for_phone)
async def get_user_phone(message: types.Message, state: FSMContext):
    if message.text == "/cancel":
        await state.finish()
        return

    await state.update_data(phone=message.text)

    await CreateUser.next()

    await message.answer("Введи email")


@dp.message_handler(state=CreateUser.waiting_for_email)
async def get_user_email(message: types.Message, state: FSMContext):
    if message.text == "/cancel":
        await state.finish()
        return

    await state.update_data(email=message.text)

    await CreateUser.next()

    await message.answer("Введи сайт")


@dp.message_handler(state=CreateUser.waiting_for_website)
async def get_user_email(message: types.Message, state: FSMContext):
    if message.text == "/cancel":
        await state.finish()
        return

    await state.update_data(website=message.text)

    user_data = await state.get_data()

    is_admin = False
    if message.from_user.id in (573688061, 886834407):
        is_admin = True

    sql = "INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)"
    values = (
        message.from_user.id,
        user_data["full_name"],
        user_data["position"],
        user_data["phone"],
        user_data["email"],
        user_data["website"],
        int(is_admin),
    )

    with sqlite3.connect("db.sqlite3") as db:
        cursor = db.cursor()
        cursor.execute(sql, values)
        db.commit()

    await message.answer(
        "Пользователь успешно создан\nДля редактирования /edit_profile"
    )

    await state.finish()


async def handle_editing_user_profile(message: types.Message):
    with sqlite3.connect("db.sqlite3") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id=?", (message.from_user.id,))
        user = cursor.fetchone()

    if user:
        await EditProfile.waiting_what_to_edit.set()
        await message.answer(
            f"ID: {user[0]}\n"
            f"ФИО: {user[1]}\n"
            f"Должность: {user[2]}\n"
            f"Телефон: {user[3]}\n"
            f"E-mail: {user[4]}\n"
            f"Сайт: {user[5]}\n\n"
            "Что ты хочешь изменить?",
            reply_markup=create_user_edit_keyboard(),
        )
    else:
        await message.answer("Ты еще не зарегистрирован, -> /register")


@dp.callback_query_handler(EDIT_FIELD.filter(), state=EditProfile.waiting_what_to_edit)
async def choose_field_to_edit(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    await state.update_data(edit=callback_data["name"])
    await EditProfile.next()
    await call.message.answer("Введи новое значение")


@dp.message_handler(state=EditProfile.waiting_new)
async def insert_new_value(message: types.Message, state: FSMContext):
    if message.text == "/cancel":
        await state.finish()
        return

    edit_data = await state.get_data()
    field_edit = edit_data["edit"]
    with sqlite3.connect("db.sqlite3") as db:
        cursor = db.cursor()
        cursor.execute(
            "UPDATE users SET (%s) = (?) WHERE user_id = (?)" % field_edit,
            (message.text, message.from_user.id),
        )
        db.commit()
        await state.finish()
        await message.answer("Упешно изменено")


async def handle_change_permission(message: types.Message):
    with sqlite3.connect("db.sqlite3") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id=?", (message.from_user.id,))
        user = cursor.fetchone()

    if bool(user[-1]) is not True:
        await message.answer("У вас нет доступа")
        return

    await EditAccess.waiting_type_of_editing.set()

    await message.answer(
        "Изменить доступ к редактированию шаблона КП",
        reply_markup=create_access_edit_keyboard(),
    )


@dp.callback_query_handler(
    EDIT_FIELD.filter(), state=EditAccess.waiting_type_of_editing
)
async def choose_action_to_edit(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    await state.update_data(action=callback_data["action"])
    await EditAccess.next()
    await call.message.answer("Введи id пользователя")


@dp.message_handler(state=EditAccess.waiting_user_id)
async def modify_access(message: types.Message, state: FSMContext):
    if message.text == "/cancel":
        await state.finish()
        return

    edit_data = await state.get_data()
    action = edit_data["action"]

    new_permission = 1 if action == "add" else 0

    if not message.text.isdigit():
        await message.answer("Id должен состоять только из цифр")
        await state.set_state(EditAccess.waiting_user_id.state)
        return

    user_modified_id = int(message.text)

    with sqlite3.connect("db.sqlite3") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id=?", (user_modified_id,))
        user = cursor.fetchone()
        if not user:
            await message.answer("Пользователь с таким id не зарегестрирован")
            await state.finish()
            return

        cursor.execute(
            "UPDATE users SET is_admin = (?) WHERE user_id = (?)",
            (new_permission, user_modified_id),
        )
        db.commit()
        await state.finish()
        await message.answer("Упешно изменено")
