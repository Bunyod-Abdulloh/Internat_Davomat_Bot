from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from keyboards.inline.student_inline_buttons import view_students_uz, teacher_attendance_check_button
from loader import dp, db
from states.teachers_state import TeacherAttendance


@dp.callback_query_handler(state=TeacherAttendance.main)
async def teacher_attendance_main_cmd(call: types.CallbackQuery, state: FSMContext):
    telegram_id = call.from_user.id
    # classes = await db.select_employee_return_list(telegram_id=telegram_id, position='Tarbiyachi')
    if call.data == "stbback":
        await call.message.delete()
    elif call.data.__contains__("absentuz_"):
        absent = call.data.split("_")[1]
        await call.answer(
            text=f"Sababsiz kelmagan o'quvchilar soni: {absent} ta", show_alert=True
        )
    elif call.data.__contains__("presentuz_"):
        present = call.data.split("_")[1]
        await call.answer(
            text=f"Kelgan o'quvchilar soni: {present} ta", show_alert=True
        )
    elif call.data.__contains__("explicableuz_"):
        explicable = call.data.split("_")[1]
        await call.answer(
            text=f"Sababli kelmagan o'quvchilar soni: {explicable} ta", show_alert=True
        )
    else:
        if call.data.__contains__("stb_"):
            student_id = call.data.split("_")[1]
            await call.answer(cache_time=0)
            get_student = await db.get_student_id(
                id_number=student_id
            )
            level = get_student[3]
            if get_student[1] == "☑️":
                await db.update_morning_check(
                    morning_check="✅", id_number=student_id
                )
            elif get_student[1] == "✅":
                await db.update_morning_check(
                    morning_check="❎", id_number=student_id
                )
            elif get_student[1] == "❎":
                await db.update_morning_check(
                    morning_check="☑️", id_number=student_id
                )
            current_date = datetime.now().date()
            get_morning = await db.get_morning(
                level=level
            )
            await call.message.edit_text(
                text=f"Sana: {current_date}\nSinf: {level}"
                     f"\n\nO'quvchilarni kelgan kelmaganligini tugmalarni bosib belgilang va yakunda "
                     f"<b>☑️ Tasdiqlash</b> tugmasini bosing!"
                     f"\n\n✅ - Kelganlar\n☑️ - Sababli kelmaganlar\n❎ - Sababsiz kelmaganlar",
                reply_markup=await view_students_uz(
                    work_time=get_morning, level=level, morning=True)
            )
        elif call.data.__contains__("next_"):
            level = call.data.split('_')[1]
            await call.message.edit_text(
                text="E'tibor qiling ✔️ Tasdiqlash tugmasini bossangiz davomat adminga boradi va buni qayta "
                     "o'zgartirib bo'lmaydi! Shu sababli ✔️ Tasdiqlash tugmasini davomatni tugatganingizga amin "
                     "bo'lganingizdan so'ng bosishingizni so'raymiz!",
                reply_markup=await teacher_attendance_check_button(level=level)
            )
            await state.finish()


@dp.callback_query_handler(F.data.contains('teachback_'), state='*')
async def back_teach_attendance(call: types.CallbackQuery):
    level = call.data.split('_')[1]
    current_date = datetime.now().date()
    get_morning = await db.get_morning(
        level=level
    )
    await call.message.edit_text(
        text=f"Sana: {current_date}\nSinf: {level}"
             f"\n\nO'quvchilarni kelgan kelmaganligini tugmalarni bosib belgilang va yakunda <b>☑️ Tasdiqlash</b> "
             f"tugmasini bosing!"
             f"\n\n✅ - Kelganlar\n☑️ - Sababli kelmaganlar\n❎ - Sababsiz kelmaganlar",
        reply_markup=await view_students_uz(
            work_time=get_morning, level=level, morning=True)
    )
    await TeacherAttendance.main.set()


@dp.callback_query_handler(F.data.contains('teachcheck_'), state='*')
async def check_teach_attendance(call: types.CallbackQuery, state: FSMContext):
    teacher_id = call.from_user.id
    level = call.data.split('_')[1]
    current_date = datetime.now().date()
    morning_students = await db.get_morning_attendance(
        level=level
    )
    for student in morning_students:
        await db.update_teacher_check(
            checked_date=current_date, check_teacher=student[1], teacher_id=teacher_id, student_id=student[0]
        )
    await call.message.edit_text(
        text="Davomat qabul qilindi!"
    )
    # await bot.send_message(
    #     chat_id=teacher[0],
    #     text="Ertalabki tarbiyachi davomatni topshirdi! Kerakli bo'limga kirib davomatni ko'rishingiz mumkin!"
    # )