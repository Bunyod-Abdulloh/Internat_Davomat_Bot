from aiogram import types
from magic_filter import F

from keyboards.default.admin_custom_buttons import admin_attendance_cbuttons
from loader import dp


@dp.message_handler(F.text == 'Davomat', state='*')
async def view_attendance_main(message: types. Message):
    await message.answer(
        text='Kerakli bo\'limni tanlang:', reply_markup=admin_attendance_cbuttons
    )


@dp.message_handler(F.text == 'Sinflar davomati')
async def view_levels_attendance(message: types.Message):
    pass


@dp.message_handler(F.text == 'Kunlik davomat')
async def view_everydays_attendance(message: types.Message):
    pass


@dp.message_handler(F.text == 'Haftalik davomat')
async def view_weekly_attendance(message: types.Message):
    pass


@dp.message_handler(F.text == 'Oylik davomat')
async def view_monthly_attendance(message: types.Message):
    pass
