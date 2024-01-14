from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.all_inline_keys import generate_multiselect_keyboard
from keyboards.inline.student_inline_buttons import view_students_uz
from loader import dp, db
from states.educators_states import EducatorsMorning


@dp.callback_query_handler(state=EducatorsMorning.main)
async def es_morning_main(call: types.CallbackQuery, state: FSMContext):
    telegram_id = call.from_user.id
    educator = await db.select_employee(telegram_id=telegram_id)
    print(educator)
    if call.data == "eik_check_uz":
        if len(educator) == 1:
            await db.add_educator(
                telegram_id=telegram_id, work_time="Ertalabki"
            )
            await call.answer(
                text="Buyrug'ingiz qabul qilindi!", show_alert=True
            )
        else:
            await call.message.edit_text(
                text="Sinflardan birini tanlang:",
                reply_markup=await generate_multiselect_keyboard(
                    telegram_id=telegram_id, table_from_db=educator, next_step=True
                )
            )
    elif call.data == "eik_attendance_uz":
        educator = await db.select_employee(
            telegram_id=call.from_user.id, onerow=True
        )
        get_morning = await db.get_morning(
            level=educator[4]
        )
        await call.message.edit_text(
            text="O'quvchilarni kelgan kelmaganligini tugmalarni bosib belgilang va yakunda <b>☑️ Tasdiqlash</b> "
                 "tugmasini bosing!"
                 "\n\n✅ - Kelganlar\n🔘 - Sababli kelmaganlar\n🟡 - Sababsiz kelmaganlar",
            reply_markup=await view_students_uz(
                work_time=get_morning, level=educator[4], morning=True)
        )
        await EducatorsMorning.attendance.set()
    elif call.data == "eik_cabinet_uz":
        pass

    elif call.data == "eik_another_uz":
        pass

    elif call.data == "eik_back_uz":
        await call.message.edit_text(
            text="Bosh sahifa"
        )
        await state.finish()
