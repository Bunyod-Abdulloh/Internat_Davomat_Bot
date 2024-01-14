import asyncio
import os

import numpy
import pandas as pd
from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

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


async def add_students_from_xls(level_data: numpy.ndarray, level: str, c: int):
    for n in level_data:
        c += 1
        first_name = n[1].split()[0]
        last_name = n[1].split()[1]
        await db.add_student(
            level=level, fullname=f"{first_name} {last_name}"
        )
        await asyncio.sleep(0.02)
    return c


@dp.message_handler(F.text == "O'quvchilarni qo'shish (excel shaklda)", state="*")
async def copy_students_from_xls(message: types.Message):
    await message.answer(
        text="Excel (xls, xlsx) shaklidagi hujjatni yuboring:"
    )
    await AdminStudents.students_xls.set()


@dp.message_handler(state=AdminStudents.students_xls, content_types=['document'])
async def get_document(message: types.Message):
    try:
        file_path = await download_and_save_file(message.document.file_id, SAVE_PATH)

        df = pd.read_excel(file_path, sheet_name=0)
        c = 0
        level = df.iat[2, 0].split()[0]

        level_check = await db.get_class_students(
            level=level
        )

        if level_check:
            await db.delete_class_students(
                level=level
            )
            c = await add_students_from_xls(
                level_data=df.values[5:], level=level, c=c
            )
        else:
            await db.add_class_employees(
                level=level
            )
            c = await add_students_from_xls(
                level_data=df.values[5:], level=level, c=c
            )

        await message.answer(
            text=f"{level} sinfi uchun jami {c} ta o'quvchi bot bazasiga qo'shildi!"
        )

        os.remove(path=file_path)

    except Exception as e:
        await message.answer(
            text=f"Xatolik! Adminga habar qiling!"
                 f"\n{e}"
        )


@dp.message_handler(F.text == "🔙 Ortga", state="*")
async def a_a_s_back(message: types.Message, state: FSMContext):
    await message.answer(
        text=message.text, reply_markup=admin_custom_btn
    )
    await state.finish()
