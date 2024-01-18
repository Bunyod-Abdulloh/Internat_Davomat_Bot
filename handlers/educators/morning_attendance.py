from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from keyboards.inline.educators_inline_keys import educators_main_uz, select_level_educators
from keyboards.inline.student_inline_buttons import view_students_uz, morning_attendance_check_button
from loader import dp, db, bot
from states.educators_states import EducatorsMorning


@dp.callback_query_handler(state=EducatorsMorning.attendance)
async def esw_morning(call: types.CallbackQuery, state: FSMContext):
    telegram_id = call.from_user.id
    classes = await db.select_employee_return_list(telegram_id=telegram_id)

    if call.data == "stbback":
        if len(classes) == 1:
            pass
        else:
            await call.message.edit_text(
                text="Sinflardan birini tanlang:",
                reply_markup=await select_level_educators()
            )
            await EducatorsMorning.first_class.set()
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

        id_number = call.data.split("_")[1]

        if call.data.__contains__("stb_"):
            await call.answer(cache_time=0)
            get_student = await db.get_student_id(
                id_number=id_number
            )

            level = get_student[3]

            if get_student[1] == "☑️":
                await db.update_morning_student(
                    morning_check="✅", id_number=id_number
                )
            elif get_student[1] == "✅":
                await db.update_morning_student(
                    morning_check="❎", id_number=id_number
                )
            elif get_student[1] == "❎":
                await db.update_morning_student(
                    morning_check="☑️", id_number=id_number
                )
            get_morning = await db.get_morning(
                level=level
            )
            await call.message.edit_text(
                text="O'quvchilarni kelgan kelmaganligini tugmalarni bosib belgilang va yakunda <b>☑️ Tasdiqlash</b> "
                     "tugmasini bosing!"
                     "\n\n✅ - Kelganlar\n\n☑️ - Sababli kelmaganlar\n\n❎ - Sababsiz kelmaganlar",
                reply_markup=await view_students_uz(
                    work_time=get_morning, level=level, morning=True)
            )
        elif call.data.__contains__("next_"):

            level = call.data.split('_')[1]
            educator_id = await db.select_employee_level(
                telegram_id=call.from_user.id, level=level
            )
            await call.message.edit_text(
                text="E'tibor qiling ✔️ Tasdiqlash tugmasini bossangiz davomat adminga boradi va buni qayta o'zgartirib "
                     "bo'lmaydi! Shu sababli ✔️ Tasdiqlash tugmasini davomatni tugatganingizga amin bo'lganingizdan "
                     "so'ng bosishingizni so'raymiz!",
                reply_markup=await morning_attendance_check_button(level=level, educator_id=educator_id[0])
            )
            await state.finish()


@dp.callback_query_handler(F.data.contains('sibback60_'), state='*')
async def back_morning_attendance(call: types.CallbackQuery):
    level = call.data.split('_')[1]
    get_morning = await db.get_morning(
        level=level
    )
    await call.message.edit_text(
        text="O'quvchilarni kelgan kelmaganligini tugmalarni bosib belgilang va yakunda <b>☑️ Tasdiqlash</b> "
             "tugmasini bosing!"
             "\n\n✅ - Kelganlar\n\n☑️ - Sababli kelmaganlar\n\n❎ - Sababsiz kelmaganlar",
        reply_markup=await view_students_uz(
            work_time=get_morning, level=level, morning=True)
    )
    await EducatorsMorning.attendance.set()


@dp.callback_query_handler(F.data.contains('sibcheck63_'), state='*')
async def ma_check_attendance(call: types.CallbackQuery):
    telegram_id = call.from_user.id
    level = call.data.split('_')[1]
    morning_students = await db.get_morning_attendance(
        level=level
    )
    for student in morning_students:
        await db.add_morning_students(
            level=level, student_id=student[0], check_educator=student[1]
        )
    await db.update_employee_attendance(
        attendance=False, level=level, telegram_id=telegram_id
    )
    teacher = await db.select_teacher_id(
        position='Teacher', level=level
    )
    await call.message.edit_text(
        text="Davomat qabul qilindi va sinf rahbariga bu haqda habar yuborildi!"
    )
    # await bot.send_message(
    #     chat_id=teacher[0],
    #     text="Ertalabki tarbiyachi davomatni topshirdi! Kerakli bo'limga kirib davomatni ko'rishingiz mumkin!"
    # )
