from aiogram import types

from keyboards.inline.admin_inline_keys import admin_view_educators_button
from loader import dp


@dp.callback_query_handler(text='admin_educatorsmain', state='*')
async def admin_educator_main(call: types.CallbackQuery):
    await call.message.edit_text(
        text="Tarbiyachilar bo'limi",
        reply_markup=await admin_view_educators_button()
    )


