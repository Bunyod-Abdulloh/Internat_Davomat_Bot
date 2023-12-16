from aiogram import types

from data.config import ADMINS
from keyboards.default.admin_custom_buttons import admin_custom_btn, admin_custom_students
from loader import dp
from states.admin_state import AdminMain


@dp.message_handler(text='/admins', state='*', user_id=ADMINS)
async def admin_main_menu(message: types.Message):
    await message.answer(
        text="Adminlar bo'limi",
        reply_markup=admin_custom_btn
    )


@dp.message_handler(text="Ota-onalar", state="*", user_id=ADMINS)
async def a_m_m_parents(message: types.Message):
    await message.answer(
        text=message.text
    )
    await AdminMain.parents.set()


@dp.message_handler(text="Sinf rahbarlar", state="*", user_id=ADMINS)
async def a_m_m_parents(message: types.Message):
    await message.answer(
        text=message.text
    )
    await AdminMain.curators.set()


@dp.message_handler(text="Tarbiyachilar", state="*", user_id=ADMINS)
async def a_m_m_parents(message: types.Message):
    await message.answer(
        text=message.text
    )
    await AdminMain.educators.set()


@dp.message_handler(text="O'quvchilar", state="*", user_id=ADMINS)
async def a_m_m_parents(message: types.Message):
    await message.answer(
        text=message.text, reply_markup=admin_custom_students
    )
    await AdminMain.students.set()
