# from aiogram import types
#
# from keyboards.inline.admin_inline_keys import
# from loader import dp, db
#
#
# @dp.message_handler(text='salom', state='*')
# async def sampler(message: types.Message):
#
#     await db.add_student(
#         student_number="1",
#         student_fullname="Aziza Abdulloh qizi",
#         class_number="6-V",
#         telegram_id=message.from_user.id
#     )
#     await message.answer(
#         text="Qo'shildi!",
#         reply_markup=await admin_main_buttons()
#     )
#
import openpyxl
from aiogram import types

from loader import dp
from states.admin_state import AdminMain, AdminStudents


@dp.message_handler(state=AdminMain.students)
async def a_a_s_students(message: types.Message):
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
            photo="AgACAgIAAxkBAAIIIWV9MW0AAZgRzdUZOs7EvKaxlmCM-QACT9cxGyhC8UsKA7-MGkMZqgEAAwIAA3gAAzME",
            caption="Diqqat!!!\n\nYuboriladigan hujjat excel jadval shaklida va yuqoridagi tartibda yozilgan bo'lishi "
                    "lozim! \n\nHujjatni yuboring:"
        )
        await AdminStudents.students_xls.set()
    elif message.text == "🔙 Ortga":
        pass


# @dp.message_handler(state=AdminStudents.students_xls)
# async def a_a_s_add_xls(message: types.Message):
#
#     await AdminStudents.download_xls.set()


@dp.message_handler(state=AdminStudents.students_xls, content_types=['document'])
async def get_photo(message: types.Message):
    await message.answer(
        text=message.document.file_id
    )

    file_name = message.document.file_name

    wb = openpyxl.load_workbook(f'D:/AbuAbdulloh/Новая папка/INTERNAT/23-24/{file_name}')

    # Получить активный лист
    sheet = wb.active

    # Получить значения из первой ячейки
    cell = sheet['A1']

    # Напечатать значение
    print(cell.value)
