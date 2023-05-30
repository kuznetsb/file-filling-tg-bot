from aiogram import types
from aiogram.utils.callback_data import CallbackData


EDIT_FIELD = CallbackData("field", "name")
EDIT_ACCESS = CallbackData("access", "action")


def create_user_edit_keyboard():
    buttons = [
        types.InlineKeyboardButton(
            text="ФИО", callback_data=EDIT_FIELD.new(name="full_name")
        ),
        types.InlineKeyboardButton(
            text="Должность", callback_data=EDIT_FIELD.new(name="position")
        ),
        types.InlineKeyboardButton(
            text="Телефон", callback_data=EDIT_FIELD.new(name="phone")
        ),
        types.InlineKeyboardButton(
            text="E-mail", callback_data=EDIT_FIELD.new(name="email")
        ),
        types.InlineKeyboardButton(
            text="Сайт", callback_data=EDIT_FIELD.new(name="website")
        ),
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard


def create_access_edit_keyboard():
    buttons = [
        types.InlineKeyboardButton(
            text="Добавить", callback_data=EDIT_ACCESS.new(action="add")
        ),
        types.InlineKeyboardButton(
            text="Убрать", callback_data=EDIT_ACCESS.new(action="delete")
        ),
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard
