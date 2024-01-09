from aiogram import types

from keyboards.inline.educators_inline_keys import educators_main_uz
from keyboards.inline.student_inline_buttons import view_students_uz
from loader import dp, db
from states.educators_states import EducatorsDiurnal


@dp.callback_query_handler(state=EducatorsDiurnal.attendance)
async def ed_attendance(call: types.CallbackQuery):
    if call.data == "stbback":
        await call.message.edit_text(
            text="Tugmalardan birini tanlang:", reply_markup=educators_main_uz
        )
        await EducatorsDiurnal.main.set()

    elif call.data.__contains__("absentuz_"):

        absent = call.data.split("_")[1]
        await call.answer(
            text=f"Qoladigan o'quvchilar soni: {absent} ta", show_alert=True
        )

    elif call.data.__contains__("presentuz_"):
        present = call.data.split("_")[1]
        await call.answer(
            text=f"Qolmaydigan o'quvchilar soni: {present} ta", show_alert=True
        )
    else:
        id_number = call.data.split("_")[1]
        get_student = await db.get_student_id(
            id_number=id_number
        )
        if call.data.__contains__("stb_"):
            await call.answer(cache_time=0)

            if get_student[1] == "🔘":
                await db.update_night_student(
                    night_check="✅",
                    id_number=id_number
                )
            elif get_student[1] == "✅":
                await db.update_night_student(
                    night_check="🔘",
                    id_number=id_number
                )
            get_night = await db.get_night(
                class_number=get_student[2]
            )
            await call.message.edit_text(
                text="Qoladigan yoki qolmaydigan o'quvchilarni tugmalarni bosib belgilang va yakunda <b>☑️ "
                     "Tasdiqlash</b> tugmasini bosing!"
                     "\n\n✅ - Qoladiganlar\n🔘 - Qolmaydiganlar",
                reply_markup=await view_students_uz(
                    work_time=get_night, class_number=get_student[2], night=True)
            )

        elif call.data.__contains__("stbcheck_"):
            await call.message.edit_text(
                text="Bosh sahifa"
            )
            await call.answer(
                text="Davomat sinf rahbariga yuborildi!", show_alert=True
            )
