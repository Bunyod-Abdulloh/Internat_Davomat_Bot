from datetime import datetime

from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from magic_filter import F

from keyboards.default.teacher_cbuttons import teachers_main_cbuttons
from keyboards.inline.all_inline_keys import teachers_multiselect_keyboard
from keyboards.inline.student_inline_buttons import view_students_uz
from loader import dp, db
from states.teachers_state import TeacherForm, TeacherAttendance


# ts_m_ = Teachers Main (handlers/teachers/file_name)
@dp.message_handler(F.text == '🏫 Sinf rahbar', state='*')
async def teachers_main_cmd(message: types.Message):
    telegram_id = message.from_user.id
    teacher = await db.select_employee_position(telegram_id=telegram_id, position='Sinf rahbar')
    if not teacher:
        await message.answer(
            text=message.text, reply_markup=ReplyKeyboardRemove()
        )
        await message.answer(
            text="O'zingizga biriktirilgan sinf yoki sinflarni tanlang:",
            reply_markup=await teachers_multiselect_keyboard(telegram_id=telegram_id)
        )
        await TeacherForm.select_class.set()
    else:
        if teacher[0] is False:
            await db.delete_employees(
                telegram_id=telegram_id, position='Sinf rahbar'
            )
            await message.answer(
                text="Ma'lumotlaringiz tasdiqlanmadi! \nIltimos ma'lumotlaringizni qayta kiriting!"
                     "\n\nO'zingizga biriktirilgan sinf yoki sinflarni tanlang:",
                reply_markup=await teachers_multiselect_keyboard(telegram_id=telegram_id)
            )
            await db.delete_employees(
                telegram_id=telegram_id, position='Sinf rahbar'
            )
            await TeacherForm.select_class.set()
        else:
            await message.answer(
                text='Kerakli bo\'limni tanlang:', reply_markup=teachers_main_cbuttons
            )

