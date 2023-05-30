from _decimal import Decimal
from dataclasses import dataclass

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import dp
from keyboards.offer_keyboard import add_specification_keyboard
from keyboards.product_keyboard import create_unit_keyboard, UNIT_TYPE


class CreateProduct(StatesGroup):
    waiting_for_product_name = State()
    waiting_for_supply_days = State()
    waiting_for_quantity = State()
    waiting_for_unit_type = State()
    waiting_for_price = State()
    waiting_for_create_product = State()


@dataclass
class Product:
    name: str
    days: int
    quantity: Decimal
    unit: str
    price: Decimal
    total: Decimal


@dp.message_handler(state=CreateProduct.waiting_for_product_name)
async def add_product_name(message: types.Message, state: FSMContext):
    if message.text == "/cancel":
        await state.finish()
        return

    await state.update_data(name=message.text)
    await CreateProduct.next()

    await message.answer("Укажите срок поставки в днях")


@dp.message_handler(state=CreateProduct.waiting_for_supply_days)
async def add_product_name(message: types.Message, state: FSMContext):
    if message.text == "/cancel":
        await state.finish()
        return

    if not message.text.isdigit():
        await message.answer(
            "Некорретный формат, поддерживаемые форматы: 1",
        )
        await state.set_state(CreateProduct.waiting_for_supply_days.state)
        return

    await state.update_data(days=int(message.text))
    await CreateProduct.next()

    await message.answer("Укажите количество (Формат: 2 или 2.00)")


@dp.message_handler(state=CreateProduct.waiting_for_quantity)
async def add_product_name(message: types.Message, state: FSMContext):
    if message.text == "/cancel":
        await state.finish()
        return

    if not message.text.replace(".", "").isdigit():
        await message.answer(
            "Некорретный формат, поддерживаемые форматы: 1 или 1.00",
        )
        await state.set_state(CreateProduct.waiting_for_quantity.state)
        return

    await state.update_data(quantity=Decimal(message.text))
    await CreateProduct.next()

    await message.answer(
        "Укажите единицу измерения", reply_markup=create_unit_keyboard()
    )


@dp.callback_query_handler(
    UNIT_TYPE.filter(), state=CreateProduct.waiting_for_unit_type
)
async def add_unit_type(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    await state.update_data(unit=callback_data["type"])
    await CreateProduct.next()

    await call.message.answer("Укажите цену за единицу (Формат: 2 или 2.00)")
    await call.answer()


@dp.message_handler(state=CreateProduct.waiting_for_price)
async def add_product_price(message: types.Message, state: FSMContext):
    if message.text == "/cancel":
        await state.finish()
        return

    if not message.text.replace(".", "").isdigit():
        await message.answer(
            "Некорретный формат, поддерживаемые форматы: 1 или 1.00",
        )
        await state.set_state(CreateProduct.waiting_for_price.state)
        return

    await state.update_data(price=Decimal(message.text))

    product_data = await state.get_data()

    total = product_data["quantity"] * product_data["price"]

    product = Product(
        name=product_data["name"],
        days=product_data["days"],
        quantity=product_data["quantity"],
        unit=product_data["unit"],
        price=product_data["price"],
        total=round(total, 2),
    )

    await state.update_data(product=product)

    await CreateProduct.next()

    await message.answer(
        "Добавлена спецификация", reply_markup=add_specification_keyboard()
    )
