from aiogram import types
from magic_filter import F

from data.config import ADMINS
from keyboards.default.admin_custom_buttons import admin_custom_btn, admin_custom_students, admin_custom_teachers
from loader import dp
from states.admin_state import AdminMain, AdminTeachers


@dp.message_handler(F.text == '/admins', state='*', user_id=ADMINS)
async def admin_main_menu(message: types.Message):
    await message.answer(
        text="Adminlar bo'limi",
        reply_markup=admin_custom_btn
    )


@dp.message_handler(F.text == "Ota-onalar", state="*", user_id=ADMINS)
async def a_m_m_parents(message: types.Message):
    await message.answer(
        text=message.text
    )
    await AdminMain.parents.set()


@dp.message_handler(F.text == "Sinf rahbarlar", state="*", user_id=ADMINS)
async def a_m_m_parents(message: types.Message):
    await message.answer(
        text=message.text
    )
    await AdminMain.curators.set()


@dp.message_handler(F.text == "O'qituvchilar", state="*", user_id=ADMINS)
async def a_m_m_teachers(message: types.Message):
    await message.answer(
        text=message.text, reply_markup=admin_custom_teachers
    )
    await AdminTeachers.main.set()


@dp.message_handler(F.text == "Tarbiyachilar", state="*", user_id=ADMINS)
async def a_m_m_parents(message: types.Message):
    await message.answer(
        text=message.text
    )
    await AdminMain.educators.set()


@dp.message_handler(F.text == "O'quvchilar", state="*", user_id=ADMINS)
async def a_m_m_parents(message: types.Message):
    await message.answer(
        text=message.text, reply_markup=admin_custom_students
    )
