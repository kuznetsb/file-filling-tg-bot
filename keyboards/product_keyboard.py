from aiogram import types
from aiogram.utils.callback_data import CallbackData


UNIT_TYPE = CallbackData("unit", "type")


def create_unit_keyboard():
    buttons = [
        types.InlineKeyboardButton(text="шт.", callback_data=UNIT_TYPE.new(type="шт.")),
        types.InlineKeyboardButton(text="кг.", callback_data=UNIT_TYPE.new(type="кг.")),
        types.InlineKeyboardButton(text="м.", callback_data=UNIT_TYPE.new(type="м.")),
        types.InlineKeyboardButton(text="км.", callback_data=UNIT_TYPE.new(type="км.")),
        types.InlineKeyboardButton(text="м2.", callback_data=UNIT_TYPE.new(type="м2.")),
        types.InlineKeyboardButton(text="м3.", callback_data=UNIT_TYPE.new(type="м3.")),
        types.InlineKeyboardButton(text="тн.", callback_data=UNIT_TYPE.new(type="тн.")),
        types.InlineKeyboardButton(text="п.м", callback_data=UNIT_TYPE.new(type="п.м")),
        types.InlineKeyboardButton(text="уп", callback_data=UNIT_TYPE.new(type="уп")),
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard
