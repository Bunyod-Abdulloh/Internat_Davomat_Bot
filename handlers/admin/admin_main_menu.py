from aiogram import types

from data.config import ADMINS
from keyboards.inline.admin_inline_keys import admin_main_button
from loader import dp


@dp.message_handler(text='/admins', state='*', user_id=ADMINS)
async def admin_main_menu(message: types.Message):
    await message.answer(
        text="Adminlar bo'limi",
        reply_markup=admin_main_button
    )
