import os.path

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from config import dp, bot
from handlers.docx_writer import PATH_TO_IMAGES, PATH_TO_COMPANY_INFO
from keyboards.template_keyboard import create_template_edit_keyboard, TEMPLATE_FIELD


class EditTemplate(StatesGroup):
    waiting_what_to_edit = State()
    waiting_new = State()


async def handle_template_edit(message: types.Message):
    await EditTemplate.waiting_what_to_edit.set()
    await message.answer("Что изменить", reply_markup=create_template_edit_keyboard())


@dp.callback_query_handler(
    TEMPLATE_FIELD.filter(), state=EditTemplate.waiting_what_to_edit
)
async def choose_field_to_edit(
    call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    await state.update_data(edit=callback_data["name"])
    await EditTemplate.next()

    if callback_data["name"] in ("logo", "sign"):
        await call.message.answer("Загрузите новое фото")
    else:
        await call.message.answer("Введите новую информацию")


@dp.message_handler(state=EditTemplate.waiting_new)
async def insert_new_value(message: types.Message, state: FSMContext):
    edit_data = await state.get_data()
    if edit_data["edit"] == "logo":
        await create_image_file(message, "logo")
    elif edit_data["edit"] == "sign":
        await create_image_file(message, "sign")
    else:
        filename = f"{edit_data['edit']}.txt"
        with open(os.path.join(PATH_TO_COMPANY_INFO, filename), "w") as file:
            file.write(message.text)

    await message.answer("Успешно изменено")
    await state.finish()


async def create_image_file(message: types.Message, filename: str):
    file_id = message.document.file_id
    resolution = message.document.file_name.split(".")[-1]
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(
        file_path, os.path.join(PATH_TO_IMAGES, f"{filename}.{resolution}")
    )
