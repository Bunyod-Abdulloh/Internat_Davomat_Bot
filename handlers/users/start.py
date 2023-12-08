from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.inline.main_menu_inline_keys import main_menu_keys
from loader import dp, db


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message):
    await message.answer(
        text="Assalomu alaykum! Internat_Botimizga xush kelibsiz!"
             "\n\nTugmalardan birini tanlang:",
        reply_markup=main_menu_keys
    )
