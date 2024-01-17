from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.educator_buttons import educators_main_buttons
from keyboards.inline.all_inline_keys import generate_multiselect_keyboard
from keyboards.inline.educators_inline_keys import select_level_educators, educators_main_uz, check_work_button
from keyboards.inline.student_inline_buttons import view_students_uz
from loader import dp, db
from states.educators_states import EducatorsMorning, EducatorsDiurnal, EducatorsAnotherClass


@dp.callback_query_handler(state=EducatorsMorning.main)
async def es_morning_main(call: types.CallbackQuery, state: FSMContext):
    telegram_id = call.from_user.id
    classes = await db.select_employee_return_list(telegram_id=telegram_id)
    attendance = await db.get_educator_morning(educator_id=classes[0][1])
    if call.data == 'main_class_uz':
        if not attendance:
            if len(classes) == 1:
                await db.add_educator(
                    educator_morning=classes[0][1], level=classes[0][0]
                )
            else:
                for class_ in classes:
                    await db.add_educator(
                        educator_morning=class_[1], level=class_[0]
                    )
            await call.answer(
                text="Buyrug'ingiz qabul qilindi va ishga kelganlar jadvalida belgilab qo'yildingiz!", show_alert=True
            )
        await call.message.answer(
            text="Tarbiyachi bo'limi", reply_markup=educators_main_buttons()
        )
        await call.message.delete()
    elif call.data == 'another_uz':
        pass
#
# else:
# pass
#     if call.data == "eik_check_uz":
#         if not attendance:
#             if len(classes) == 1:
#                 await db.add_educator(
#                     educator_morning=classes[0][1], level=classes[0][0]
#                 )
#             else:
#                 for class_ in classes:
#                     await db.add_educator(
#                         educator_morning=class_[1], level=class_[0]
#                     )
#         await call.answer(
#             text="Buyrug'ingiz qabul qilindi!", show_alert=True
#         )
#     elif call.data == "eik_attendance_uz":

#     elif call.data == "eik_cabinet_uz":
#         pass
#
#     elif call.data == "eik_another_uz":
#         await call.message.edit_text(
#             text="Ishlamoqchi bo'lgan sinfingizni tanlang:",
#             reply_markup=await generate_multiselect_keyboard(telegram_id=telegram_id, another=True)
#         )
#         await EducatorsAnotherClass.main.set()
#
#     elif call.data == "eik_back_uz":
#         await call.message.edit_text(
#             text="Bosh sahifa"
#         )
#         await state.finish()


@dp.callback_query_handler(state=EducatorsMorning.first_class)
async def ma_first_class(call: types.CallbackQuery):
    if call.data == "back":
        await call.message.answer(
            text="Tarbiyachi bo'limi", reply_markup=educators_main_buttons()
        )
        await call.message.delete()
    else:
        level = call.data
        get_morning = await db.get_morning(
            level=level
        )
        await call.message.edit_text(
            text="O'quvchilarni kelgan kelmaganligini tugmalarni bosib belgilang va yakunda <b>☑️ Tasdiqlash</b> "
                 "tugmasini bosing!"
                 "\n\n✅ - Kelganlar\n\n☑️ - Sababli kelmaganlar\n\n❎ - Sababsiz kelmaganlar",
            reply_markup=await view_students_uz(
                work_time=get_morning, level=level, morning=True)
        )
        await EducatorsMorning.attendance.set()
