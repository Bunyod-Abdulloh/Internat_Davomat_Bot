from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.admin_inline_keys import key_returner
from keyboards.inline.educators_inline_keys import educators_class_btn, edu_work_time
from keyboards.inline.student_inline_buttons import students_button
from loader import dp, db
from states.educators_states import EducatorsWorkTime, EducatorsQuestionnaire


# e_w_t_ = Educators Work Time (handlers/educators/work_time)
@dp.callback_query_handler(state=EducatorsWorkTime.main)
async def e_w_t_main(call: types.CallbackQuery, state: FSMContext):
    if call.data == "edu_back":
        await call.message.edit_text(
            text="O'zingizga biriktirilgan sinfni tanlang:", reply_markup=await educators_class_btn()
        )
        await EducatorsQuestionnaire.select_class.set()

    elif call.data.__contains__("edumorning_"):
        class_number = call.data.split("_")[-1]

        absent = await db.count_mark(class_number=class_number, mark="✅")
        present = await db.count_mark(class_number=class_number, mark="❎")
        await call.message.edit_text(
            text="O'quvchilarni kelgan kelmaganligini tugmalarni bosib belgilang va yakunda <b>☑️ Tasdiqlash</b> "
                 "tugmasini bosing:",
            reply_markup=await students_button(
                class_number=class_number, back="Ortga", check="Tasdiqlash", absent=f"Kelganlar: {absent} ta",
                present=f"Kelmaganlar: {present} ta", attendance_uz=True
            )
        )
        await state.update_data(
            count=0
        )
        await EducatorsWorkTime.morning.set()

    elif call.data.__contains__("eduhalf_"):
        class_number = call.data.split("_")[-1]

    elif call.data.__contains__("eduday_"):
        class_number = call.data.split("_")[-1]


@dp.callback_query_handler(state=EducatorsWorkTime.morning)
async def e_w_t_morning(call: types.CallbackQuery, state: FSMContext):

    if call.data == "absent_uz":
        await call.answer(
            text="Bu tugma faqat kelgan o'quvchilar sonini ko'rsatadi!", show_alert=True
        )

    elif call.data == "present_uz":
        await call.answer(
            text=f"Bu tugma faqat kelmagan o'quvchilar sonini ko'rsatadi!", show_alert=True
        )
    else:
        await call.answer(cache_time=0)
        data = await state.get_data()
        count = data['count']
        class_number = call.data.split("_")[-1]
        student_id = call.data.split("_")[1]

        if call.data.__contains__("stbback_"):
            await call.message.edit_text(
                text="Ish vaqtingizni tanlang:",
                reply_markup=await edu_work_time(class_number=class_number, morning="Ertalabki", half_day="Yarim kun",
                                                 all_day="To'liq kun", back="Ortga")
            )
            await EducatorsWorkTime.main.set()
        elif call.data.__contains__("stb_"):
            get_student = await db.get_student_id(
                id_number=student_id
            )
            count += 1
            if count == 1:
                if get_student[-1] == "✅":
                    await db.update_mark_student(
                        mark="🔘",
                        id_number=student_id
                    )
                else:
                    await db.update_mark_student(
                        mark="✅",
                        id_number=student_id
                    )

            elif count == 2:
                if get_student[-1] == "🔘":
                    await db.update_mark_student(
                        mark="✅",
                        id_number=student_id
                    )
                else:
                    await db.update_mark_student(
                        mark="🔘",
                        id_number=student_id
                    )
                count = 0

            await state.update_data(
                count=count
            )
            absent = await db.count_mark(class_number=class_number, mark="✅")
            present = await db.count_mark(class_number=class_number, mark="🔘")
            await call.message.edit_text(
                text="O'quvchilarni kelgan kelmaganligini tugmalarni bosib belgilang va yakunda <b>☑️ Tasdiqlash</b> "
                     "tugmasini bosing:",
                reply_markup=await students_button(
                    class_number=class_number, back="Ortga", check="Tasdiqlash", absent=f"Kelganlar: {absent} ta",
                    present=f"Kelmaganlar: {present} ta", attendance_uz=True
                )
            )

        elif call.data.__contains__("stbcheck_"):

            print(call.data)


# @dp.callback_query_handler(state=EducatorsWorkTime.morning)
# async def e_w_t_present_absent(call: types.CallbackQuery):
#
#     if call.data == "absent_uz":
#         await call.answer(
#             text="Bu tugma faqat kelgan o'quvchilar sonini ko'rsatadi!", show_alert=True
#         )
#
#     elif call.data == "present_uz":
#         await call.answer(
#             text=f"Bu tugma faqat kelmagan o'quvchilar sonini ko'rsatadi!", show_alert=True
#         )
