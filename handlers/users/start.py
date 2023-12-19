from aiogram import types, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import ADMINS
from keyboards.default.start_keyboard import menu
from keyboards.inline.main_menu_inline_keys import main_menu_keys
from loader import dp, db, bot


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message):
    print(message.from_user.full_name)
    await message.answer(
        text="Assalomu alaykum! Internat_Botimizga xush kelibsiz!",
        reply_markup=menu
    )
    await message.answer(
        text="Tugmalardan birini tanlang:",
        reply_markup=main_menu_keys
    )


@dp.message_handler(text="🏡 Bosh sahifa", state="*")
async def main_menu_custom(message: types.Message, state: FSMContext):

    await message.answer(
        text="Kerakli bo'limni tanlang:", reply_markup=main_menu_keys
    )
    await state.finish()

    # await message.answer(
    #     text="Live location yuboring"
    # )


@dp.message_handler(content_types=['location'], state="*")
async def live_location(message: types.Message):
    for admin in ADMINS:
        await bot.send_location(
            chat_id=admin,
            latitude=message.location.latitude,
            longitude=message.location.longitude
        )
