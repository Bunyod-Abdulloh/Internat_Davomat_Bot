from aiogram import types

from loader import dp


@dp.message_handler(F.text == "", state="*")
async def a_a_l_add_lessons(message: types.Message):


