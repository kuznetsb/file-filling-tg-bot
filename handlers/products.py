from dataclasses import dataclass

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import dp
from keyboards.offer_keyboard import add_specification_keyboard
from keyboards.product_keyboard import create_unit_keyboard, UNIT_TYPE


class CreateProduct(StatesGroup):
    waiting_for_product_name = State()
    waiting_for_quantity = State()
    waiting_for_unit_type = State()
    waiting_for_price = State()
    waiting_for_create_product = State()


@dataclass
class Product:
    name: str
    quantity: str
    unit: str
    price: str


@dp.message_handler(state=CreateProduct.waiting_for_product_name)
async def add_product_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await CreateProduct.next()

    await message.answer("Укажите количество")


@dp.message_handler(state=CreateProduct.waiting_for_quantity)
async def add_product_name(message: types.Message, state: FSMContext):
    await state.update_data(quantity=message.text)
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

    await call.message.answer("Укажите цену за единицу")
    await call.answer()


@dp.message_handler(state=CreateProduct.waiting_for_price)
async def add_product_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)

    product_data = await state.get_data()
    product = Product(
        name=product_data["name"],
        quantity=product_data["quantity"],
        unit=product_data["unit"],
        price=product_data["price"],
    )

    await state.update_data(product=product)

    await CreateProduct.next()

    await message.answer(
        "Добавлена спецификация", reply_markup=add_specification_keyboard()
    )
