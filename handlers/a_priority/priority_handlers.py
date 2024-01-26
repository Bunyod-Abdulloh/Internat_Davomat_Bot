from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Command
from magic_filter import F

from keyboards.default.main_menu_cbuttons import main_menu_uz
from keyboards.inline.main_menu_inline_keys import select_language_ikeys
from loader import dp


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message):
    print(message.from_user.full_name)
    await message.answer(
        text="Tugmalardan birini tanlang:",
        reply_markup=main_menu_uz
    )


@dp.message_handler(F.text == "🏡 Bosh sahifa", state="*")
async def main_menu_custom(message: types.Message, state: FSMContext):
    await message.answer(
        text="Kerakli bo'limni tanlang:", reply_markup=main_menu_uz
    )
    await state.finish()
