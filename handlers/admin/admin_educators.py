from aiogram import types

from keyboards.inline.admin_inline_keys import admin_view_educators_button, edit_educators
from loader import dp, db


#  a_e = Admin educator (handlers/admin/file_name)
@dp.callback_query_handler(text='aik_educatorsmain', state='*')
async def a_e_main(call: types.CallbackQuery):
    await call.message.edit_text(
        text="Tarbiyachilar bo'limi",
        reply_markup=await admin_view_educators_button()
    )


@dp.callback_query_handler(text_contains='aikeducatorid_', state='*')
async def a_e_get_educator_id(call: types.CallbackQuery):
    educator_id = call.data.split('_')[-1]
    educator = await db.select_educator(
        telegram_id=educator_id
    )
    if educator[3] is None:
        await call.message.edit_text(
            text=f"Hodim: {educator[1]}"
                 f"\nLavozimi: {educator[8]}"
                 f"\nTelefon raqami: {educator[2]}"
                 f"\nBiriktirilgan sinfi: {educator[4]}",
            reply_markup=await edit_educators(
                telegram_id=educator_id
            )
        )


