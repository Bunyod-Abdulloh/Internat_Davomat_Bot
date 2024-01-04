from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.main_menu_cbuttons import main_menu_uz
from keyboards.inline.educators_inline_keys import edu_work_time
from keyboards.inline.student_inline_buttons import view_students_uz
from loader import dp, db
from states.educators_states import EducatorsWorkTime


@dp.callback_query_handler(text="eik_attendance_uz", state="*")
async def ema_main(call: types.CallbackQuery):
    educator = await db.select_educator(
        telegram_id=call.from_user.id, onerow=True
    )
    get_morning = await db.get_students(
        class_number=educator[4]
    )
    await call.message.edit_text(
        text="O'quvchilarni kelgan kelmaganligini tugmalarni bosib belgilang va yakunda <b>☑️ Tasdiqlash</b> "
             "tugmasini bosing!"
             "\n\n✅ - Kelganlar\n🔘 - Sababli kelmaganlar\n🟡 - Sababsiz kelmaganlar",
        reply_markup=await view_students_uz(
            work_time=get_morning, class_number=educator[4])
    )
    await EducatorsWorkTime.morning.set()


@dp.callback_query_handler(state=EducatorsWorkTime.morning)
async def esw_morning(call: types.CallbackQuery, state: FSMContext):
    if call.data == "absent_uz":
        await call.answer(
            text="Bu tugma faqat kelgan/kelmagan o'quvchilar sonini ko'rsatadi!", show_alert=True
        )
    elif call.data == "eik_back_uz":
        pass
        # await call.message.edit_text(
        #     text="Ish vaqtingizni tanlang:",
        #     reply_markup=await edu_work_time(class_number=class_number, morning="Ertalabki", half_day="Yarim kun",
        #                                      all_day="To'liq kun", back="Ortga")
        # )
        await EducatorsWorkTime.presents.set()
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

            get_morning = await db.get_students(
                class_number=class_number
            )
            await call.message.edit_text(
                text="O'quvchilarni kelgan kelmaganligini tugmalarni bosib belgilang va yakunda <b>☑️ Tasdiqlash</b> "
                     "tugmasini bosing!"
                     "\n\n✅ - Kelganlar\n🔘 - Sababli kelmaganlar\n🟡 - Sababsiz kelmaganlar",
                reply_markup=await view_students_uz(
                    work_time=get_morning, class_number=class_number)
            )

        elif call.data.__contains__("stbcheck_"):
            await call.message.edit_text(
                text="Bosh sahifa"
            )
            await call.answer(
                text="Davomat sinf rahbariga yuborildi!", show_alert=True
            )
