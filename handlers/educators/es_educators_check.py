from datetime import datetime

from aiogram import types

from loader import dp, db


@dp.callback_query_handler(text="eik_check_uz", state="*")
async def ech_main(call: types.CallbackQuery):

    current_hour = datetime.now().hour

    if current_hour >= 6:
        if current_hour < 10:
            await db.update_educator_morning(
                morning=True, telegram_id=call.from_user.id
            )
            await call.answer(
                text="Buyrug'ingiz qabul qilindi va bu haqda admin ogohlantirildi!", show_alert=True
            )
        elif current_hour > 10 <= 18:
            await db.update_educator_day(
                day=True, telegram_id=call.from_user.id
            )
            await call.answer(
                text="Buyrug'ingiz qabul qilindi va bu haqda admin ogohlantirildi!", show_alert=True
            )
        else:
            await call.answer(
                text="Bu tugma faqat ish vaqtingizda ishlaydi!", show_alert=True
            )
    educator = await db.select_educator(
        telegram_id=call.from_user.id
    )
