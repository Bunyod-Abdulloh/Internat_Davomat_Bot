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
        print("another ishladi")
    elif call.data == "back":
        await call.message.edit_text(
            text="Tarbiyachi bo'limi"
        )
        await state.finish()
    else:
        level = call.data
        attendance = await db.get_educator_morning(
            educator_telegram=telegram_id, level=level, checked_date=datetime.now().date()
        )
        if attendance:
            await db.delete_attendance_class(
                telegram_id=telegram_id, level=level
            )
        else:
            await db.add_educator(
                educator_telegram=telegram_id, level=level, check_educator="☀️"
            )
        await call.message.edit_text(
            text="Ishlamoqchi bo'lgan sinf yoki sinflaringizni tanlang:"
                 "\n\n(mabodo fikringizdan qaytib qolsangiz iltimos ishlamaydigan sinfingizni ustiga bosib ☑️ holatiga "
                 "keltirib qo'ying!)",
            reply_markup=await select_level_educators(telegram_id=telegram_id, another=True, next_step=True)
        )
