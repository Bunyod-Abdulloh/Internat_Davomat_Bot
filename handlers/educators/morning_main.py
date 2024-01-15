from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.all_inline_keys import generate_multiselect_keyboard
from keyboards.inline.educators_inline_keys import select_level_educators, educators_main_uz
from keyboards.inline.student_inline_buttons import view_students_uz
from loader import dp, db
from states.educators_states import EducatorsMorning, EducatorsDiurnal


@dp.callback_query_handler(state=EducatorsMorning.main)
async def es_morning_main(call: types.CallbackQuery, state: FSMContext):

    telegram_id = call.from_user.id
    classes = await db.select_employee_return_list(telegram_id=telegram_id)
    attendance = await db.get_educator_morning(educator_id=classes[0][1])

    if call.data == "eik_check_uz":
        if not attendance:
            if len(classes) == 1:
                await db.add_educator(
                    educator_morning=classes[0][1], level=classes[0][0]
                )
            else:
                for class_ in classes:
                    await db.add_educator(
                        educator_morning=class_[1], level=class_[0]
                    )
        await call.answer(
            text="Buyrug'ingiz qabul qilindi!", show_alert=True
        )
    elif call.data == "eik_attendance_uz":
        if len(classes) == 1:
            educator = await db.select_employee(
                telegram_id=telegram_id
            )
            level = educator[0]
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
        else:
            await call.message.edit_text(
                text="Sinflardan birini tanlang:",
                reply_markup=await select_level_educators(
                    classes=classes
                )
            )
            await EducatorsMorning.first_class.set()
    elif call.data == "eik_cabinet_uz":
        pass

    elif call.data == "eik_another_uz":
        pass

    elif call.data == "eik_back_uz":
        await call.message.edit_text(
            text="Bosh sahifa"
        )
        await state.finish()


@dp.callback_query_handler(state=EducatorsMorning.first_class)
async def ma_first_class(call: types.CallbackQuery):
    if call.data == "back":
        await call.message.edit_text(
            text="Tugmalardan birini tanlang:", reply_markup=educators_main_uz
        )
        await EducatorsMorning.main.set()
    else:
        level = call.data
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
