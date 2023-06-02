from aiogram import types
from aiogram.utils.callback_data import CallbackData


TEMPLATE_FIELD = CallbackData("field", "name")


def create_template_edit_keyboard():
    buttons = [
        types.InlineKeyboardButton(
            text="Логотип", callback_data=TEMPLATE_FIELD.new(name="logo")
        ),
        types.InlineKeyboardButton(
            text="Реквизиты КП", callback_data=TEMPLATE_FIELD.new(name="requisites")
        ),
        types.InlineKeyboardButton(
            text="Заголовок КП", callback_data=TEMPLATE_FIELD.new(name="offer_header")
        ),
        types.InlineKeyboardButton(
            text="Описание КП",
            callback_data=TEMPLATE_FIELD.new(name="offer_description"),
        ),
        types.InlineKeyboardButton(
            text="Инфо руководителя КП",
            callback_data=TEMPLATE_FIELD.new(name="ceo_info"),
        ),
        types.InlineKeyboardButton(
            text="Печать КП", callback_data=TEMPLATE_FIELD.new(name="sign")
        ),
        types.InlineKeyboardButton(
            text="Реквизиты СЧЕТ",
            callback_data=TEMPLATE_FIELD.new(name="invoice_company_info"),
        ),
        types.InlineKeyboardButton(
            text="Заголовок СЧЕТ",
            callback_data=TEMPLATE_FIELD.new(name="invoice_header"),
        ),
        types.InlineKeyboardButton(
            text="Инфо руководителя СЧЕТ",
            callback_data=TEMPLATE_FIELD.new(name="ceo_accountant_info"),
        ),
        types.InlineKeyboardButton(
            text="Печать СЧЕТ", callback_data=TEMPLATE_FIELD.new(name="sign_invoice")
        ),
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard
