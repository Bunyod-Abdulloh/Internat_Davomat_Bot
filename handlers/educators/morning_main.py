from datetime import datetime

from aiogram import types
from loader import dp, db
from aiogram.dispatcher import FSMContext
from states.educators_states import EducatorsMorning, EducatorsAnotherClass
from keyboards.default.educator_buttons import educators_main_buttons
from keyboards.inline.educators_inline_keys import select_level_educators, another_class_buttons
from keyboards.inline.student_inline_buttons import view_students_uz


@dp.callback_query_handler(state=EducatorsMorning.main)
async def es_morning_main(call: types.CallbackQuery, state: FSMContext):
    telegram_id = call.from_user.id
    classes = await db.select_employee_return_list(telegram_id=telegram_id, position='Tarbiyachi')
    educator_verification = await db.select_check_work_telegram(telegram_id=telegram_id)
    if call.data == 'main_class_uz':
        if not educator_verification:
            if len(classes) == 1:
                level = classes[0][0]
                await db.add_employee_checker(telegram_id=telegram_id, level=level, check_work=True)
            else:
                for class_ in classes:
                    await db.add_employee_checker(telegram_id=telegram_id, level=class_[0], check_work=True)
        await call.answer(
            text="Buyrug'ingiz qabul qilindi va ishga kelganlar jadvalida belgilab qo'yildingiz!", show_alert=True
        )
        await call.message.answer(
            text="Tarbiyachi bo'limi", reply_markup=educators_main_buttons()
        )
        await call.message.delete()

    elif call.data == 'another_uz':
        if educator_verification:
            await call.answer(
                text="Siz boshqa sinf/sinflarga kelganligingiz haqida habar qoldirib bo'lgansiz! O'zgartirish uchun "
                     "Shaxsiy kabinetingizga kirishingiz lozim!", show_alert=True
            )
            await state.finish()
            await call.message.delete()
        else:
            await call.message.edit_text(
                text="Ishlamoqchi bo'lgan sinf yoki sinflaringizni tanlang:",
                reply_markup=await another_class_buttons(telegram_id=telegram_id)
            )
            await EducatorsAnotherClass.main.set()
