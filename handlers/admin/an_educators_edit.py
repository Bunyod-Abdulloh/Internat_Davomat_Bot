from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.admin.a_functions import educator_main_first, educator_main_second
from keyboards.inline.admin_edit_educator_buttons import edit_educators
from keyboards.inline.admin_inline_keys import admin_check_keyboard, admin_view_educators_btn
from loader import dp, db
from states.admin_state import AdminEditEdicators


# a_e_e = Admin educator edit (handlers/admin/file-name)
@dp.callback_query_handler(state=AdminEditEdicators.main)
async def a_e_e_main(call: types.CallbackQuery, state: FSMContext):

    id_number = call.data.split("_")[-1]
    educator = await db.select_by_id(
        id_number=id_number
    )
    await state.update_data(
        educator_id=id_number
    )
    if call.data.__contains__("aeebname_"):
        await call.message.edit_text(
            text=f"Hodim joriy ism-familiyasi: {educator[1]}"
                 f"\n\nO'zgartirmoqchi bo'lgan ism-familiyangizni kiriting:"
        )
        await AdminEditEdicators.edit_fullname.set()

    # elif call.data.__contains__("")


@dp.message_handler(state=AdminEditEdicators.edit_fullname)
async def a_e_e_fullname(message: types.Message, state: FSMContext):
    await state.update_data(
        educator_fullname=message.text
    )
    await message.answer(
        text="Kiritilgan ma'lumotlarni tasdiqlaysizmi?",
        reply_markup=admin_check_keyboard
    )
    await AdminEditEdicators.check_fullname.set()


@dp.callback_query_handler(state=AdminEditEdicators.check_fullname)
async def a_e_e_check_fullname(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    fullname = data['educator_fullname']
    id_number = data['educator_id']

    if call.data == "checkadmin":
        await db.update_educator_fullname(
            fullname=fullname, id_number=id_number
        )

        await call.answer(
            text="Ma'lumotlar o'zgartirildi!",
            show_alert=True
        )

    elif call.data == "canceladmin":
        await call.answer(
            text="Amaliyot bekor qilindi!",
            show_alert=True
        )

    await call.message.edit_text(
        text="Tarbiyachilar bo'limi",
        reply_markup=await admin_view_educators_btn()
    )
