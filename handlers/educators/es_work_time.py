from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.educators_inline_keys import educators_main_uz
from keyboards.inline.student_inline_buttons import view_students_uz
from loader import dp, db
from states.educators_states import EducatorsWorkTime, EducatorsMain


# ewt_ = Educators Work Time (handlers/educators/work_time)

@dp.callback_query_handler(state=EducatorsWorkTime.presents)
async def ewt_main(call: types.CallbackQuery, state: FSMContext):
    level = call.data.split("_")[-1]

    if call.data.__contains__("eduback_"):
        await call.message.edit_text(
            text="Kerakli bo'limni tanlang:", reply_markup=educators_main_uz
        )
        await EducatorsMain.main.set()

    elif call.data.__contains__("edumorning_"):
        status = await db.select_admins()

        if status[0] is True:

            get_morning = await db.get_morning(
                level=level
            )            

            absent = await db.count_morning_check(level=level, morning_check="✅")
            present = await db.count_morning_check(level=level, morning_check="🔘")
            explicable = await db.count_morning_check(level=level, morning_check="🟡")
            await call.message.edit_text(
                text="O'quvchilarni kelgan kelmaganligini tugmalarni bosib belgilang va yakunda <b>☑️ Tasdiqlash</b> "
                     "tugmasini bosing!"
                     "\n\n✅ - Kelganlar\n🔘 - Sababli kelmaganlar\n🟡 - Sababsiz kelmaganlar",
                reply_markup=await view_students_uz(
                    work_time=get_morning, level=level, back="Ortga", check="Tasdiqlash",
                    absent=f"✅ : {absent} ta", explicable=f"🟡 : {explicable} ta", present=f"🔘 : {present} ta", uz=True
                )
            )
            await EducatorsWorkTime.morning.set()
        else:
            await call.message.edit_text(
                text="Botning ushbu qismi vaqtincha o'chirilgan! Profilaktika ishlari yakuniga yetgach qayta yoqiladi!"
            )

    elif call.data.__contains__("eduhalf_"):
        status = await db.select_admins()

        if status[0] is True:
            level = call.data.split("_")[-1]
        else:
            await call.message.edit_text(
                text="Botning ushbu qismi vaqtincha o'chirilgan! Profilaktika ishlari yakuniga yetgach qayta yoqiladi!"
            )

    elif call.data.__contains__("eduday_"):
        status = await db.select_admins()
        if status[0] is True:
            level = call.data.split("_")[-1]
        else:
            await call.message.edit_text(
                text="Botning ushbu qismi vaqtincha o'chirilgan! Profilaktika ishlari yakuniga yetgach qayta yoqiladi!"
            )

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
