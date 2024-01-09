import asyncio
import os
import pandas as pd
from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.default.admin_custom_buttons import admin_custom_btn
from loader import dp, db, bot
from states.admin_state import AdminMain, AdminStudents


SAVE_PATH = 'downloads/'


async def download_and_save_file(file_id: str, save_path: str):

    file_info = await bot.get_file(file_id)
    file_path = os.path.join(save_path, file_info.file_path)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    await bot.download_file(file_info.file_path, file_path)

    return file_path


@dp.message_handler(state=AdminMain.students)
async def a_a_s_students(message: types.Message, state: FSMContext):
    if message.text == "Sinf qo'shish":
        await AdminStudents.add_class.set()

    elif message.text == "Sinf o'chirish":
        await AdminStudents.delete_class.set()

    elif message.text == "O'quvchi qo'shish":
        await AdminStudents.add_student.set()

    elif message.text == "O'quvchi o'chirish":
        await AdminStudents.delete_student.set()

    elif message.text == "O'quvchilarni qo'shish (excel shaklda)":
        await message.answer(
            text="Yuboriladigan hujjat yo'lini yuboring:"
        )
        await AdminStudents.students_xls.set()

    elif message.text == "🔙 Ortga":
        await message.answer(
            text=message.text, reply_markup=admin_custom_btn
        )
        await state.finish()


@dp.message_handler(state=AdminStudents.students_xls, content_types=['document'])
async def get_document(message: types.Message):
    try:
        file_path = await download_and_save_file(message.document.file_id, SAVE_PATH)

        df = pd.read_excel(file_path, sheet_name=0)

        level = df.iat[2, 0].split()[0]

        c = 0

        for n in df.values[5:]:
            c += 1
            first_name = n[1].split()[0]
            last_name = n[1].split()[1]
            await db.add_student(
                class_number=level, fullname=f"{first_name} {last_name}"
            )
            await asyncio.sleep(0.05)

        await message.answer(
            text=f"{level} sinfi uchun jami {c} ta o'quvchi bot bazasiga qo'shildi!"
        )

        os.remove(path=file_path)

    except Exception as e:
        await message.answer(
            text=f"Xatolik! Adminga habar qiling!"
                 f"\n{e}"
        )


@dp.message_handler(state=AdminStudents.students_xls, text="🔙 Ortga")
async def a_a_s_back(message: types.Message, state: FSMContext):
    await message.answer(
        text=message.text, reply_markup=admin_custom_btn
    )
    await state.finish()


@dp.message_handler(state="*", content_types=['photo'], user_id=ADMINS)
async def a_a_photo(message: types.Message):
    await message.answer(
        text=message.photo[-1].file_id
    )
