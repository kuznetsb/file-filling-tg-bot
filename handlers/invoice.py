import os
from _decimal import Decimal
from dataclasses import dataclass
from datetime import datetime, date

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from config import dp
from handlers.docx_writer import PATH_TO_IMAGES
from handlers.invoice_docx import form_docx_invoice, PATH_TO_INVOICE
from handlers.products import Product, CreateProduct
from keyboards.invoice_keyboard import (
    create_date_keyboard,
    CALLBACK_DATE,
    create_receiver_keyboard,
    RECEIVER_TYPE,
    create_total_keyboard,
    TOTAL_TYPE,
)
from keyboards.offer_keyboard import (
    add_products_keyboard,
    ADD_PRODUCT,
    ADD_SPEC,
    CALLBACK_VAT,
    create_vat_keyboard,
    choice_file_format,
    FILE_FORMAT,
)


class MakeInvoice(StatesGroup):
    waiting_for_vat = State()
    waiting_for_invoice_num = State()
    waiting_for_date = State()
    waiting_for_custom_date = State()
    waiting_for_buyer = State()
    waiting_for_receiver = State()
    waiting_for_custom_receiver = State()
    waiting_for_products = State()
    waiting_for_total_decide = State()
    waiting_for_total = State()
    waiting_for_invoice_creating = State()


@dataclass
class Invoice:
    vat: str
    number: str
    date: datetime
    buyer: str
    receiver: str
    products: list[Product]
    total: Decimal
    total_text: str | None


async def handle_invoice_creation(message: types.Message):
    await MakeInvoice.waiting_for_vat.set()
    await message.answer("Выберите НДС", reply_markup=create_vat_keyboard())


@dp.callback_query_handler(CALLBACK_VAT.filter(), state=MakeInvoice.waiting_for_vat)
async def handle_vat_type(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    await state.update_data(vat=callback_data["percentage"])

    await MakeInvoice.next()
    await call.message.answer("Укажите номер счета\nПример: 1234 или 1234-1")
    await call.answer()


@dp.message_handler(state=MakeInvoice.waiting_for_invoice_num)
async def get_offer_number(message: types.Message, state: FSMContext):
    if message.text == "/cancel":
        await state.finish()
        return

    await state.update_data(invoice_num=message.text)

    await MakeInvoice.next()

    await message.answer(
        "Укажите дату выставления счета",
        reply_markup=create_date_keyboard(),
    )


@dp.callback_query_handler(CALLBACK_DATE.filter(), state=MakeInvoice.waiting_for_date)
async def handle_date(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    if callback_data["type"] == "today":
        today = date.today()
        await state.update_data(date=today)
        await state.set_state(MakeInvoice.waiting_for_buyer.state)
        await call.message.answer("Укажите данные покупателя")
    else:
        await MakeInvoice.next()
        await call.message.answer("Введите дату\nПример: 01.05.2023")

    await call.answer()


@dp.message_handler(state=MakeInvoice.waiting_for_custom_date)
async def get_manual_date(message: types.Message, state: FSMContext):
    if message.text == "/cancel":
        await state.finish()
        return

    custom_date = datetime.strptime(message.text, "%d.%m.%Y")
    await state.update_data(date=custom_date)

    await MakeInvoice.next()

    await message.answer("Укажите данные покупателя")


@dp.message_handler(state=MakeInvoice.waiting_for_buyer)
async def get_buyer_info(message: types.Message, state: FSMContext):
    if message.text == "/cancel":
        await state.finish()
        return

    await state.update_data(buyer=message.text)

    await MakeInvoice.next()

    await message.answer(
        "Укажите данные грузополучателя", reply_markup=create_receiver_keyboard()
    )


@dp.callback_query_handler(
    RECEIVER_TYPE.filter(), state=MakeInvoice.waiting_for_receiver
)
async def get_receiver_info(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    if callback_data["type"] == "same":
        invoice_data = await state.get_data()
        await state.update_data(receiver=invoice_data["buyer"])
        await state.set_state(MakeInvoice.waiting_for_products.state)
        await call.message.answer(
            "Добавление товаров в счет", reply_markup=add_products_keyboard()
        )

    else:
        await MakeInvoice.next()
        await call.message.answer("Введите данные грузополучателя")

    await call.answer()


@dp.message_handler(state=MakeInvoice.waiting_for_custom_receiver)
async def get_manual_date(message: types.Message, state: FSMContext):
    if message.text == "/cancel":
        await state.finish()
        return

    await state.update_data(receiver=message.text)

    await MakeInvoice.next()

    await message.answer(
        "Добавление товаров в счет", reply_markup=add_products_keyboard()
    )


@dp.callback_query_handler(ADD_PRODUCT.filter(), state=MakeInvoice.waiting_for_products)
async def add_product(
    call: types.CallbackQuery,
    callback_data: dict,
    state: FSMContext,
):
    await CreateProduct.waiting_for_product_name.set()

    await call.message.answer("Укажите наименование")
    await call.answer()


@dp.callback_query_handler(
    ADD_SPEC.filter(), state=CreateProduct.waiting_for_create_product
)
async def add_specification(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    product_data = await state.get_data()
    product = product_data["product"]

    await MakeInvoice.waiting_for_products.set()
    invoice_data = await state.get_data()
    products = invoice_data.get("products")
    if not products:
        products = [product]
    else:
        products.append(product)

    if callback_data["action"] == "complete":
        total = sum(product.total for product in products)
        invoice = Invoice(
            vat=invoice_data["vat"],
            number=invoice_data["invoice_num"],
            date=invoice_data["date"],
            buyer=invoice_data["buyer"],
            receiver=invoice_data["receiver"],
            products=products,
            total=round(total, 2),
            total_text=None,
        )
        await state.update_data(invoice=invoice)
        await MakeInvoice.next()

        await call.message.answer(
            f"Сумма: {invoice.total}\n Введите ее прописью:",
            reply_markup=create_total_keyboard(),
        )

    elif callback_data["action"] == "add":
        await state.update_data(products=products)
        await CreateProduct.waiting_for_product_name.set()

        await call.message.answer("Укажите наименование")
        await call.answer()


@dp.callback_query_handler(
    TOTAL_TYPE.filter(), state=MakeInvoice.waiting_for_total_decide
)
async def decide_total_type(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    if callback_data["action"] == "skip":
        await MakeInvoice.next()
        await MakeInvoice.next()
        await call.message.answer("Выберите формат", reply_markup=choice_file_format())
        await call.answer()
        return

    await MakeInvoice.next()
    await call.message.answer(
        "Введите сумму (Например: Девятьсот тысяч двести рублей 00 копеек"
    )
    await call.answer()


@dp.message_handler(state=MakeInvoice.waiting_for_total)
async def get_manual_date(message: types.Message, state: FSMContext):
    invoice_data = await state.get_data()
    invoice = invoice_data["invoice"]
    invoice.total_text = message.text

    await state.update_data(invoice=invoice)

    await MakeInvoice.next()

    await message.answer("Выберите формат", reply_markup=choice_file_format())


@dp.callback_query_handler(
    FILE_FORMAT.filter(), state=MakeInvoice.waiting_for_invoice_creating
)
async def generate_invoice(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    if callback_data["format"] == "cancel":
        await state.finish()
        return

    invoice_data = await state.get_data()
    invoice = invoice_data["invoice"]
    invoice_filename = invoice.number

    if callback_data["format"] == "docx":
        create_docx_invoice(invoice)

        with open(
            os.path.join(PATH_TO_INVOICE, f"СЧЕТ-{invoice_filename}.docx"), "rb"
        ) as file:
            await call.message.reply_document(file)

        os.remove(os.path.join(PATH_TO_INVOICE, f"СЧЕТ-{invoice_filename}.docx"))


def create_docx_invoice(invoice: Invoice):
    invoice_filename = invoice.number

    image_names = os.listdir(PATH_TO_IMAGES)

    logo_filename = ""
    sign_filename = ""

    for file in image_names:
        if file.startswith("logo"):
            logo_filename = file
        elif file.startswith("invoice_sign"):
            sign_filename = file

    form_docx_invoice(invoice, invoice_filename, logo_filename, sign_filename)
