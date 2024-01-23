from datetime import datetime

from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from magic_filter import F
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
        await db.add_employee_sql(
            telegram_id=telegram_id, position='Sinf rahbar'
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
            current_date = datetime.now().date()
            checker = await db.select_check_work_teacher(
                checked_date=current_date, level=teacher[1]
            )
            if checker is None:
                await message.answer(
                    text='Davomat hozircha mavjud emas!'
                )
            else:
                level = teacher[1]
                current_date = datetime.now().date()
                get_morning = await db.get_morning(
                    level=level
                )
                await message.answer(
                        text=f"Sana: {current_date}\nSinf: {level}"
                             f"\n\nO'quvchilarni kelgan kelmaganligini tugmalarni bosib belgilang va yakunda "
                             f"<b>☑️ Tasdiqlash</b> tugmasini bosing!"
                             f"\n\n✅ - Kelganlar\n☑️ - Sababli kelmaganlar\n❎ - Sababsiz kelmaganlar",
                        reply_markup=await view_students_uz(
                            work_time=get_morning, level=level, morning=True)
                    )
                await TeacherAttendance.main.set()
