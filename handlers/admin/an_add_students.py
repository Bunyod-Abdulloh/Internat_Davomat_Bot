import openpyxl
from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.admin_custom_buttons import admin_custom_btn
from loader import dp, db
from states.admin_state import AdminMain, AdminStudents


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
        await message.answer_photo(
            photo="AgACAgIAAxkBAAIJYmV9jU0nJmkk94-SvPbmsf6T0UGPAAKq2DEbKELxS1ajHyqGhCkDAQADAgADeAADMwQ",
            caption="Diqqat!!!\n\nYuboriladigan hujjat excel jadval shaklida va yuqoridagi tartibda yozilgan bo'lishi "
                    "lozim! \n\nHujjatni yuboring:"
        )
        await AdminStudents.students_xls.set()

    elif message.text == "🔙 Ortga":
        await message.answer(
            text=message.text, reply_markup=admin_custom_btn
        )
        await state.finish()


@dp.message_handler(state=AdminStudents.students_xls, content_types=['document'])
async def get_photo(message: types.Message):
    await message.answer(
        text=message.document.file_id
    )

    file_name = message.document.file_name

    wb = openpyxl.load_workbook(f'D:/AbuAbdulloh/Новая папка/INTERNAT/23-24/{file_name}')

    sheet = wb.active
    c = 0
    level = str()
    for row in sheet.iter_rows():
        c += 1
        class_number = row[1].value
        fullname = row[2].value
        level = class_number
        await db.add_student(
            class_number=class_number, fullname=fullname
        )
    await message.answer(
        text=f"{level} sinfi uchun jami qo'shilgan o'quvchilar soni: {c} ta"
    )
    c = 0
    level = ''
    await AdminMain.students.set()


@dp.message_handler(state=AdminStudents.students_xls, text="🔙 Ortga")
async def a_a_s_back(message: types.Message, state: FSMContext):
    await message.answer(
        text=message.text, reply_markup=admin_custom_btn
    )
    await state.finish()
