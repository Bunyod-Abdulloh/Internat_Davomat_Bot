from aiogram import types

from keyboards.inline.educators_inline_keys import educators_main_uz
from keyboards.inline.student_inline_buttons import view_students_uz
from loader import dp, db
from states.educators_states import EducatorsMorning


@dp.callback_query_handler(state=EducatorsMorning.attendance)
async def esw_morning(call: types.CallbackQuery):

    if call.data == "stbback":
        await call.message.edit_text(
            text="Tugmalardan birini tanlang:", reply_markup=educators_main_uz
        )
        await EducatorsMorning.main.set()

    elif call.data.__contains__("absentuz_"):

        absent = call.data.split("_")[1]
        await call.answer(
            text=f"Kelgan o'quvchilar soni: {absent} ta", show_alert=True
        )

    elif call.data.__contains__("presentuz_"):
        present = call.data.split("_")[1]
        await call.answer(
            text=f"Sababli kelmagan o'quvchilar soni: {present} ta", show_alert=True
        )

    elif call.data.__contains__("explicableuz_"):
        explicable = call.data.split("_")[1]
        await call.answer(
            text=f"Sababsiz kelmagan o'quvchilar soni: {explicable} ta", show_alert=True
        )

    else:
        class_number = call.data.split("_")[-1]
        id_number = call.data.split("_")[1]

        if call.data.__contains__("stb_"):
            await call.answer(cache_time=0)
            get_student = await db.get_student_id(
                id_number=id_number
            )

            if get_student[0] == "🔘":
                await db.update_morning_student(
                    morning_check="✅",
                    id_number=id_number
                )
            elif get_student[0] == "✅":
                await db.update_morning_student(
                    morning_check="🟡",
                    id_number=id_number
                )
            elif get_student[0] == "🟡":
                await db.update_morning_student(
                    morning_check="🔘",
                    id_number=id_number
                )

            get_morning = await db.get_morning(
                class_number=class_number
            )
            await call.message.edit_text(
                text="O'quvchilarni kelgan kelmaganligini tugmalarni bosib belgilang va yakunda <b>☑️ Tasdiqlash</b> "
                     "tugmasini bosing!"
                     "\n\n✅ - Kelganlar\n🔘 - Sababli kelmaganlar\n🟡 - Sababsiz kelmaganlar",
                reply_markup=await view_students_uz(
                    work_time=get_morning, class_number=class_number, morning=True)
            )

        elif call.data.__contains__("stbcheck_"):
            await call.message.edit_text(
                text="Bosh sahifa"
            )
            await call.answer(
                text="Davomat sinf rahbariga yuborildi!", show_alert=True
            )
