from aiogram import executor, types
from aiogram.dispatcher import FSMContext

from config import dp
from handlers.offer import handle_offer_creation
from handlers.users import handle_user_creation, handle_editing_user_profile


async def set_default_commands(dispatcher):
    await dispatcher.bot.set_my_commands(
        [
            types.BotCommand("cancel", "Отмена"),
            types.BotCommand("register", "Регистрация"),
            types.BotCommand("createoffer", "Создать КП"),
            types.BotCommand("editprofile", "Редактировать профиль"),
        ]
    )


@dp.message_handler(commands=["createoffer"])
async def create_offer(message: types.Message):
    await handle_offer_creation(message)


@dp.message_handler(commands=["register"])
async def create_profile(message: types.Message):
    await handle_user_creation(message)


@dp.message_handler(commands=["editprofile"])
async def edit_profile(message: types.Message):
    await handle_editing_user_profile(message)


@dp.message_handler(commands=["cancel"], state="*")
async def cancel_state(message: types.Message, state: FSMContext):
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=set_default_commands)
