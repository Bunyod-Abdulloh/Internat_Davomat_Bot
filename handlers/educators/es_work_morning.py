from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.educators_inline_keys import edu_work_time
from keyboards.inline.student_inline_buttons import view_students_uz
from loader import dp, db
from states.educators_states import EducatorsWorkTime


@dp.callback_query_handler(state=EducatorsWorkTime.morning)
async def esw_morning(call: types.CallbackQuery, state: FSMContext):

    if call.data == "absent_uz":
        await call.answer(
            text="Bu tugma faqat kelgan/kelmagan o'quvchilar sonini ko'rsatadi!", show_alert=True
        )
    else:
        await call.answer(cache_time=0)
        data = await state.get_data()
        count = data['count']
        class_number = call.data.split("_")[-1]
        id_number = call.data.split("_")[1]

        if call.data.__contains__("stbback_"):
            await call.message.edit_text(
                text="Ish vaqtingizni tanlang:",
                reply_markup=await edu_work_time(class_number=class_number, morning="Ertalabki", half_day="Yarim kun",
                                                 all_day="To'liq kun", back="Ortga")
            )
            await EducatorsWorkTime.presents.set()
        elif call.data.__contains__("stb_"):
            get_student = await db.get_student_id(
                id_number=id_number
            )

            count += 1
            if count == 1:
                if get_student[0] == "✅":
                    await db.update_morning_student(
                        morning_check="🔘",
                        id_number=id_number
                    )
                else:
                    await db.update_morning_student(
                        morning_check="✅",
                        id_number=id_number
                    )

            elif count == 2:
                if get_student[0] == "🔘":
                    await db.update_morning_student(
                        morning_check="✅",
                        id_number=id_number
                    )
                else:
                    await db.update_morning_student(
                        morning_check="🔘",
                        id_number=id_number
                    )
                count = 0

            await state.update_data(
                count=count
            )
            absent = await db.count_morning_check(class_number=class_number, morning_check="✅")
            present = await db.count_morning_check(class_number=class_number, morning_check="🔘")
            get_morning = await db.get_students(
                class_number=class_number
            )
            await call.message.edit_text(
                text="O'quvchilarni kelgan kelmaganligini tugmalarni bosib belgilang va yakunda <b>☑️ Tasdiqlash</b> "
                     "tugmasini bosing:",
                reply_markup=await view_students_uz(
                    work_time=get_morning, class_number=class_number, back="Ortga", check="Tasdiqlash",
                    absent=f"🔘 : {absent} ta", present=f"✅ : {present} ta", uz=True
                )
            )

        elif call.data.__contains__("stbcheck_"):
            print(call.data)
