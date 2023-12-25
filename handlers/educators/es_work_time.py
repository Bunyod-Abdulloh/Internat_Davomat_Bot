from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.admin_inline_keys import key_returner
from keyboards.inline.educators_inline_keys import educators_class_btn, edu_work_time
from keyboards.inline.student_inline_buttons import view_students_uz
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
        status = await db.select_admins()

        if status[0] is True:
            class_number = call.data.split("_")[-1]
            morning = await db.get_students(
                class_number=class_number
            )            

            absent = await db.count_morning_check(class_number=class_number, morning_check="✅")
            present = await db.count_morning_check(class_number=class_number, morning_check="🔘")
            await call.message.edit_text(
                text="O'quvchilarni kelgan kelmaganligini tugmalarni bosib belgilang va yakunda <b>☑️ Tasdiqlash</b> "
                     "tugmasini bosing:",
                reply_markup=await view_students_uz(
                    work_time=morning, class_number=class_number, back="Ortga", check="Tasdiqlash",
                    absent=f"Kelganlar: {absent} ta", present=f"Kelmaganlar: {present} ta"
                )
            )
            await state.update_data(
                count=0
            )
            await EducatorsWorkTime.morning.set()
        else:
            await call.message.edit_text(
                text="Botning ushbu qismi vaqtincha o'chirilgan! Profilaktika ishlari yakuniga yetgach qayta yoqiladi!"
            )

    elif call.data.__contains__("eduhalf_"):
        status = await db.select_admins()

        if status[0] is True:
            class_number = call.data.split("_")[-1]
        else:
            await call.message.edit_text(
                text="Botning ushbu qismi vaqtincha o'chirilgan! Profilaktika ishlari yakuniga yetgach qayta yoqiladi!"
            )

    elif call.data.__contains__("eduday_"):
        status = await db.select_admins()
        if status[0] is True:
            class_number = call.data.split("_")[-1]
        else:
            await call.message.edit_text(
                text="Botning ushbu qismi vaqtincha o'chirilgan! Profilaktika ishlari yakuniga yetgach qayta yoqiladi!"
            )


@dp.callback_query_handler(state=EducatorsWorkTime.morning)
async def e_w_t_morning(call: types.CallbackQuery, state: FSMContext):

    if call.data == "absent_uz" or call.data == "present_uz":
        await call.answer(
            text="Bu tugma faqat kelgan o'quvchilar sonini ko'rsatadi!", show_alert=True
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
            await EducatorsWorkTime.main.set()
        elif call.data.__contains__("stb_"):
            get_morning = await db.get_student_id(
                id_number=id_number
            )

            count += 1
            if count == 1:
                if get_morning[0] == "✅":
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
                if get_morning[0] == "🔘":
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
            morning = await db.get_students(
                class_number=class_number
            )
            await call.message.edit_text(
                text="O'quvchilarni kelgan kelmaganligini tugmalarni bosib belgilang va yakunda <b>☑️ Tasdiqlash</b> "
                     "tugmasini bosing:",
                reply_markup=await view_students_uz(
                    work_time=morning, class_number=class_number, back="Ortga", check="Tasdiqlash", 
                    absent=f"Kelganlar: {absent} ta", present=f"Kelmaganlar: {present} ta"
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
