from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.student_inline_buttons import view_students_uz
from loader import dp, db
from states.educators_states import EducatorsMorning


@dp.callback_query_handler(state=EducatorsMorning.main)
async def es_morning_main(call: types.CallbackQuery, state: FSMContext):

    if call.data == "eik_check_uz":
        await db.update_educator_morning(
            morning=True, telegram_id=call.from_user.id
        )
        await call.answer(
            text="Buyrug'ingiz qabul qilindi!", show_alert=True
        )
    elif call.data == "eik_attendance_uz":
        educator = await db.select_educator(
            telegram_id=call.from_user.id, onerow=True
        )
        get_morning = await db.get_morning(
            class_number=educator[4]
        )
        await call.message.edit_text(
            text="O'quvchilarni kelgan kelmaganligini tugmalarni bosib belgilang va yakunda <b>☑️ Tasdiqlash</b> "
                 "tugmasini bosing!"
                 "\n\n✅ - Kelganlar\n🔘 - Sababli kelmaganlar\n🟡 - Sababsiz kelmaganlar",
            reply_markup=await view_students_uz(
                work_time=get_morning, class_number=educator[4], morning=True)
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
