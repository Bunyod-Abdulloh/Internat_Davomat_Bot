from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from keyboards.default.educator_buttons import educators_main_buttons
from keyboards.inline.educators_inline_keys import select_level_educators
from keyboards.inline.student_inline_buttons import view_students_uz, morning_attendance_check_button
from loader import dp, db, bot
from states.educators_states import EducatorsMorning


@dp.callback_query_handler(state=EducatorsMorning.attendance)
async def esw_morning(call: types.CallbackQuery, state: FSMContext):
    telegram_id = call.from_user.id
    classes = await db.select_employee_return_list(telegram_id=telegram_id, position='Tarbiyachi')
    if call.data == "stbback":
        if len(classes) == 1:
            await call.message.answer(
                text="Tarbiyachi bo'limi", reply_markup=educators_main_buttons()
            )
            await call.message.delete()
        else:
            await call.message.edit_text(
                text="Sinflardan birini tanlang:",
                reply_markup=await select_level_educators(telegram_id=telegram_id)
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
        if call.data.__contains__("stb_"):
            id_number = call.data.split("_")[1]
            await call.answer(cache_time=0)
            get_student = await db.get_student_id(
                id_number=id_number
            )
            level = get_student[3]
            if get_student[1] == "☑️":
                await db.update_morning_check(
                    morning_check="✅", id_number=id_number
                )
            elif get_student[1] == "✅":
                await db.update_morning_check(
                    morning_check="❎", id_number=id_number
                )
            elif get_student[1] == "❎":
                await db.update_morning_check(
                    morning_check="☑️", id_number=id_number
                )
            get_morning = await db.get_morning(
                level=level
            )
            current_date = datetime.now().date()
            await call.message.edit_text(
                text=f"Sana: {current_date}\nSinf: {level}\nJami o'quvchilar soni: {len(get_morning)} ta"
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
                reply_markup=await morning_attendance_check_button(level=level)
            )
            await state.finish()


@dp.callback_query_handler(F.data.contains('sibback60_'), state='*')
async def back_morning_attendance(call: types.CallbackQuery):
    level = call.data.split('_')[1]
    current_date = datetime.now().date()
    get_morning = await db.get_morning(
        level=level
    )
    await call.message.edit_text(
        text=f"Sana: {current_date}\nSinf: {level}"
             f"\n\nO'quvchilarni kelgan kelmaganligini tugmalarni bosib belgilang va yakunda <b>☑️ Tasdiqlash</b> "
             f"tugmasini bosing!"
             f"\n\n✅ - Kelganlar\n\n☑️ - Sababli kelmaganlar\n\n❎ - Sababsiz kelmaganlar",
        reply_markup=await view_students_uz(
            work_time=get_morning, level=level, morning=True)
    )
    await EducatorsMorning.attendance.set()


@dp.callback_query_handler(F.data.contains('sibcheck63_'), state='*')
async def ma_check_attendance(call: types.CallbackQuery):
    telegram_id = call.from_user.id
    level = call.data.split('_')[1]
    levels = await db.select_all_classes()

    morning_students = await db.get_morning_attendance(
        level=level
    )
    for n in levels:
        level_ = f'{n[0]}-{n[1]}'
        for student in morning_students:
            await db.add_morning_students(
                level=level_, student_id=student[0], morning_id=telegram_id,
                check_morning=student[1], check_teacher=student[1]
            )
    # await db.check_employee_attendance(
    #     check_attendance=True,  telegram_id=telegram_id, level=level
    # )
    teacher = await db.select_teacher_id(
        position='Sinf rahbar', level=level
    )
    await call.message.edit_text(
        text="Davomat qabul qilindi va sinf rahbariga bu haqda habar yuborildi!"
    )
    # await bot.send_message(
    #     chat_id=teacher[0],
    #     text="Ertalabki tarbiyachi davomatni topshirdi! Kerakli bo'limga kirib davomatni ko'rishingiz mumkin!"
    # )
