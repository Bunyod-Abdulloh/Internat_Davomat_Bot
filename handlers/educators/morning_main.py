from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.educator_buttons import educators_main_buttons
from keyboards.inline.educators_inline_keys import select_level_educators
from keyboards.inline.student_inline_buttons import view_students_uz
from loader import dp, db
from states.educators_states import EducatorsMorning, EducatorsAnotherClass


@dp.callback_query_handler(state=EducatorsMorning.main)
async def es_morning_main(call: types.CallbackQuery, state: FSMContext):
    telegram_id = call.from_user.id
    current_date = datetime.now().date()
    classes = await db.select_employee_return_list(telegram_id=telegram_id)
    attendance = await db.get_educator_morning(
        educator_telegram=telegram_id, checked_date=current_date, level=classes[0][0]
    )
    if call.data == 'main_class_uz':
        if not attendance:
            if len(classes) == 1:
                await db.add_educator(
                    educator_telegram=telegram_id, level=classes[0][0], check_educator="☀️"
                )
            else:
                for class_ in classes:
                    await db.add_educator(
                        educator_telegram=telegram_id, level=class_[0], check_educator="☀️"
                    )
        await call.answer(
            text="Buyrug'ingiz qabul qilindi va ishga kelganlar jadvalida belgilab qo'yildingiz!", show_alert=True
        )
        await call.message.answer(
            text="Tarbiyachi bo'limi", reply_markup=educators_main_buttons()
        )
        await call.message.delete()

    elif call.data == 'another_uz':
        if attendance:
            await call.answer(
                text="Siz boshqa sinf/sinflarga kelganligingiz haqida habar qoldirib bo'lgansiz! O'zgartirish uchun "
                     "Shaxsiy kabinetingizga kirishingiz lozim!", show_alert=True
            )
            await state.finish()
            await call.message.delete()
        else:
            await call.message.edit_text(
                text="Ishlamoqchi bo'lgan sinf yoki sinflaringizni tanlang:",
                reply_markup=await select_level_educators(telegram_id=telegram_id, another=True)
            )
            await EducatorsAnotherClass.main.set()


@dp.callback_query_handler(state=EducatorsMorning.first_class)
async def ma_first_class(call: types.CallbackQuery):
    if call.data == "back":
        await call.message.answer(
            text="Tarbiyachi bo'limi", reply_markup=educators_main_buttons()
        )
        await call.message.delete()
    else:
        level = call.data
        employee_attendance = await db.select_employee_level(telegram_id=call.from_user.id, level=level)
        if employee_attendance[2] is False:
            await call.answer(
                text="Siz ushbu sinfni yo'qlama qilib bo'lgansiz!", show_alert=True
            )
        else:
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
