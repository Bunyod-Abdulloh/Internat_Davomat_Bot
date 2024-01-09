from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.student_inline_buttons import view_students_uz
from loader import dp, db
from states.educators_states import EducatorsDiurnal


@dp.callback_query_handler(state=EducatorsDiurnal.main)
async def es_diurnal_main(call: types.CallbackQuery, state: FSMContext):
    if call.data == "eik_check_uz":
        await db.update_educator_day(
            day=True, telegram_id=call.from_user.id
        )
        await call.answer(
            text="Buyrug'ingiz qabul qilindi!", show_alert=True
        )
    elif call.data == "eik_attendance_uz":
        educator = await db.select_educator(
            telegram_id=call.from_user.id, onerow=True
        )
        get_night = await db.get_night(
            class_number=educator[4]
        )
        await call.message.edit_text(
            text="Qoladigan yoki qolmaydigan o'quvchilarni tugmalarni bosib belgilang va yakunda <b>☑️ Tasdiqlash</b> "
                 "tugmasini bosing!"
                 "\n\n✅ - Qoladiganlar\n🔘 - Qolmaydiganlar",
            reply_markup=await view_students_uz(
                work_time=get_night, class_number=educator[4], night=True)
        )
        await EducatorsDiurnal.attendance.set()
    elif call.data == "eik_cabinet_uz":
        pass

    elif call.data == "eik_another_uz":
        pass

    elif call.data == "eik_back_uz":
        await call.message.edit_text(
            text="Bosh sahifa"
        )
        await state.finish()

