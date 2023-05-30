from aiogram import types
from aiogram.utils.callback_data import CallbackData


TEMPLATE_FIELD = CallbackData("field", "name")


def create_template_edit_keyboard():
    buttons = [
        types.InlineKeyboardButton(
            text="Логотип", callback_data=TEMPLATE_FIELD.new(name="logo")
        ),
        types.InlineKeyboardButton(
            text="Реквизиты", callback_data=TEMPLATE_FIELD.new(name="requisites")
        ),
        types.InlineKeyboardButton(
            text="Заглавье КП", callback_data=TEMPLATE_FIELD.new(name="offer_header")
        ),
        types.InlineKeyboardButton(
            text="Описание КП",
            callback_data=TEMPLATE_FIELD.new(name="offer_description"),
        ),
        types.InlineKeyboardButton(
            text="Инфо руководителя", callback_data=TEMPLATE_FIELD.new(name="ceo_info")
        ),
        types.InlineKeyboardButton(
            text="Печать", callback_data=TEMPLATE_FIELD.new(name="sign")
        ),
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard
