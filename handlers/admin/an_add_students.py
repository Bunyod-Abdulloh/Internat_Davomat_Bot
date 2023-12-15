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
from aiogram import types

from loader import dp
from states.admin_state import AdminMain


@dp.message_handler(state=AdminMain.students)
async def a_a_s_students(message: types.Message):
    if message.text == "Sinf qo'shish":
        pass
    elif message.text == "O'quvchi qo'shish":
        pass
    elif message.text == "🔙 Ortga":
        pass
