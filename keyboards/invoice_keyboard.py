from aiogram import types
from aiogram.utils.callback_data import CallbackData

CALLBACK_DATE = CallbackData("date", "type")
RECEIVER_TYPE = CallbackData("receiver", "type")
TOTAL_TYPE = CallbackData("type", "action")


def create_date_keyboard():
    buttons = [
        types.InlineKeyboardButton(
            text="Сегодняшняя", callback_data=CALLBACK_DATE.new(type="today")
        ),
        types.InlineKeyboardButton(
            text="Ввести вручную",
            callback_data=CALLBACK_DATE.new(type="custom"),
        ),
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard


def create_receiver_keyboard():
    buttons = [
        types.InlineKeyboardButton(
            text="Как и покупатель", callback_data=RECEIVER_TYPE.new(type="same")
        ),
        types.InlineKeyboardButton(
            text="Другой",
            callback_data=RECEIVER_TYPE.new(type="another"),
        ),
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard


def create_total_keyboard():
    buttons = [
        types.InlineKeyboardButton(
            text="Ввести вручную", callback_data=TOTAL_TYPE.new(action="manual")
        ),
        types.InlineKeyboardButton(
            text="Пропустить",
            callback_data=TOTAL_TYPE.new(action="skip"),
        ),
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard
