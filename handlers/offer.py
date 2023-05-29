import sqlite3
from dataclasses import dataclass

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from handlers.docx_writer import form_docx_offer
from handlers.products import CreateProduct, Product
from keyboards.offer_keyboard import (
    create_vat_keyboard,
    CALLBACK_VAT,
    create_supply_type_keyboard,
    SUPPLY_TYPE,
    add_products_keyboard,
    ADD_PRODUCT,
    ADD_SPEC,
    choice_file_format,
    FILE_FORMAT,
)
from config import dp


class MakeOffer(StatesGroup):
    waiting_for_vat_type = State()
    waiting_for_delivery_type = State()
    waiting_for_offer_num = State()
    waiting_for_goods = State()
    waiting_for_create_offer = State()


@dataclass
class Offer:
    number: str
    supply_type: str
    vat: str
    products: list[Product]


@dataclass
class User:
    full_name: str
    position: str
    phone: str
    email: str
    website: str


async def handle_offer_creation(message: types.Message):
    await MakeOffer.waiting_for_vat_type.set()
    await message.answer("Выберите тип НДС", reply_markup=create_vat_keyboard())


@dp.callback_query_handler(CALLBACK_VAT.filter(), state=MakeOffer.waiting_for_vat_type)
async def handle_vat_type(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    await state.update_data(vat=callback_data["percentage"])

    await MakeOffer.next()
    await call.message.answer(
        "Выберите тип поставки", reply_markup=create_supply_type_keyboard()
    )
    await call.answer()


@dp.callback_query_handler(
    SUPPLY_TYPE.filter(), state=MakeOffer.waiting_for_delivery_type
)
async def handle_supply_type(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    await state.update_data(supply_type=callback_data["type"])
    await MakeOffer.next()
    await call.message.answer("Укажите номер КП")
    await call.answer()


@dp.message_handler(state=MakeOffer.waiting_for_offer_num)
async def get_offer_number(message: types.Message, state: FSMContext):
    await state.update_data(offer_num=message.text)

    await MakeOffer.next()

    await message.answer(
        "Добавление товаров в коммерческое предложение",
        reply_markup=add_products_keyboard(),
    )


@dp.callback_query_handler(ADD_PRODUCT.filter(), state=MakeOffer.waiting_for_goods)
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

    await MakeOffer.waiting_for_goods.set()
    offer_data = await state.get_data()
    products = offer_data.get("products")
    if not products:
        products = [product]
    else:
        products.append(product)

    if callback_data["action"] == "complete":
        offer = Offer(
            number=offer_data["offer_num"],
            supply_type=offer_data["supply_type"],
            vat=offer_data["vat"],
            products=products,
        )
        await state.update_data(offer=offer)
        await MakeOffer.next()

        await call.message.answer("Выберите формат", reply_markup=choice_file_format())

    elif callback_data["action"] == "add":
        await state.update_data(products=products)
        await CreateProduct.waiting_for_product_name.set()

        await call.message.answer("Укажите наименование")
        await call.answer()


@dp.callback_query_handler(
    FILE_FORMAT.filter(), state=MakeOffer.waiting_for_create_offer
)
async def generate_offer(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    if callback_data["format"] == "cancel":
        await state.finish()
        return

    offer_data = await state.get_data()
    offer = offer_data["offer"]

    if callback_data["format"] == "docx":
        user = get_user_instance(call.from_user.id)
        docx_offer = form_docx_offer(offer, user)

    elif callback_data["format"] == "pdf":
        pass


def get_user_instance(user_id: int) -> User:
    with sqlite3.connect("db.sqlite3") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        user_info = cursor.fetchone()

    return User(
        full_name=user_info[1],
        position=user_info[2],
        phone=user_info[3],
        email=user_info[4],
        website=user_info[5],
    )
