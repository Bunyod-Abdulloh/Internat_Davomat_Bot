from aiogram import types, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import ADMINS
from keyboards.inline.main_menu_inline_keys import main_menu_keys
from loader import dp, db, bot


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message):
    await message.answer(
        text="Assalomu alaykum! Internat_Botimizga xush kelibsiz!"
             "\n\nTugmalardan birini tanlang:",
        reply_markup=main_menu_keys
    )
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
