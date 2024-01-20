from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.educators_inline_keys import select_level_educators
from loader import dp, db
from states.educators_states import EducatorsAnotherClass


@dp.callback_query_handler(state=EducatorsAnotherClass.main)
async def e_another_class(call: types.CallbackQuery, state: FSMContext):
    telegram_id = call.from_user.id
    if call.data == "check_another_uz":
        await call.message.edit_text(
            text="Buyrug'ingiz qabul qilindi va ishga kelganlar ro'yxatiga kiritildingiz!"
        )
        await state.finish()
    elif call.data == "back":
        await db.delete_checker(telegram_id=telegram_id)
        await call.message.edit_text(
            text="Tarbiyachi bo'limi"
        )
        await state.finish()
    else:
        level = call.data
        attendance = await db.select_check_work(telegram_id=telegram_id, level=level)
        print(attendance)
        if attendance:
            await db.delete_checker_class(telegram_id=telegram_id, level=level)
        else:
            await db.add_employee_checker(
                telegram_id=telegram_id, level=level, check_work=True
            )
        await call.message.edit_text(
            text="Ishlamoqchi bo'lgan sinf yoki sinflaringizni tanlang:"
                 "\n\n(mabodo fikringizdan qaytib qolsangiz iltimos ishlamaydigan sinfingizni ustiga bosib ☑️ holatiga "
                 "keltirib qo'ying!)",
            reply_markup=await select_level_educators(telegram_id=telegram_id, another=True, next_step=True)
        )
