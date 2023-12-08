from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.admin_edit_educator_buttons import edit_educators
from keyboards.inline.admin_inline_keys import admin_view_educators_button, admin_main_button
from loader import dp, db
from states.admin_state import AdminEditEdicators


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

    educator = await db.select_by_id(
        id_number=educator_id
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
    else:
        await call.message.edit_text(
            text=f"Hodim: {educator[1]}"
                 f"\nLavozimi: {educator[8]}"
                 f"\nTelefon raqami: {educator[2]}"
                 f"\nIkkinchi telefon raqami: {educator[3]}"
                 f"\nBiriktirilgan sinfi: {educator[4]}",
            reply_markup=await edit_educators(
                telegram_id=educator_id,
                second_phone=True
            )
        )
    await AdminEditEdicators.main.set()


@dp.callback_query_handler(text="aikback_adminpage", state="*")
async def a_e_back_adminpage(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        text="Admin bosh menyusi",
        reply_markup=admin_main_button
    )
    await state.finish()


@dp.callback_query_handler(text="aeeb_educatorslist", state="*")
async def a_e_educatorslist(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        text="Tarbiyachilar bo'limi",
        reply_markup=await admin_view_educators_button()
    )
    await state.finish()
