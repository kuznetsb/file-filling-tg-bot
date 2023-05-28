from aiogram import types
from aiogram.utils.callback_data import CallbackData


CALLBACK_VAT = CallbackData("vat", "percentage")
SUPPLY_TYPE = CallbackData("supply", "type")
ADD_PRODUCT = CallbackData("product", "action")
ADD_SPEC = CallbackData("spec", "action")
FILE_FORMAT = CallbackData("file", "format")


def create_vat_keyboard():
    buttons = [
        types.InlineKeyboardButton(
            text="Без НДС", callback_data=CALLBACK_VAT.new(percentage="Без НДС")
        ),
        types.InlineKeyboardButton(
            text="10%", callback_data=CALLBACK_VAT.new(percentage="10%")
        ),
        types.InlineKeyboardButton(
            text="20%", callback_data=CALLBACK_VAT.new(percentage="20%")
        ),
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard


def create_supply_type_keyboard():
    buttons = [
        types.InlineKeyboardButton(
            text="Оборудование", callback_data=SUPPLY_TYPE.new(type="Оборудование")
        ),
        types.InlineKeyboardButton(
            text="Продукция", callback_data=SUPPLY_TYPE.new(type="Продукция")
        ),
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard


def add_products_keyboard():
    button = types.InlineKeyboardButton(
        text="Добавить", callback_data=ADD_PRODUCT.new(action="add")
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(button)
    return keyboard


def add_specification_keyboard():
    buttons = [
        types.InlineKeyboardButton(
            text="Добавить", callback_data=ADD_SPEC.new(action="add")
        ),
        types.InlineKeyboardButton(
            text="Завершить", callback_data=ADD_SPEC.new(action="complete")
        ),
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard


def choice_file_format():
    buttons = [
        types.InlineKeyboardButton(
            text="DOCX", callback_data=FILE_FORMAT.new(format="docx")
        ),
        types.InlineKeyboardButton(
            text="PDF", callback_data=FILE_FORMAT.new(format="pdf")
        ),
        types.InlineKeyboardButton(
            text="Отмена", callback_data=FILE_FORMAT.new(format="cancel")
        ),
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard
