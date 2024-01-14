from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from data.config import ADMINS
from keyboards.default.main_menu_cbuttons import main_menu_uz
from keyboards.inline.admin_inline_keys import admin_check_keyboard, admin_check_btn
from loader import dp, db, bot
from states.admin_state import AdminEducator_State


# a_e_a - Admin educators add (handlers/file_name)


@dp.message_handler(commands=["new_employees"], user_id=ADMINS[0], state="*")
async def new_employee_main(message: types.Message):
    new_employees = await db.select_new_employees(access=False)
    if new_employees:
        for employee in new_employees:
            if employee[-2] is None:
                await message.answer(
                    text=f"Lavozim: {employee[4]}"
                         f"\n\nIsm sharif: {employee[3]}"
                         f"\n\nTelefon raqam: {employee[5]}"
                         f"\n\nBiriktirilgan sinf: {employee[2]}",
                    reply_markup=await admin_check_btn(
                        user_id=employee[1]
                    )
                )
            else:
                await message.answer(
                    text=f"Lavozim: {employee[4]}"
                         f"\n\nIsm sharif: {employee[3]}"
                         f"\n\nTelefon raqam: {employee[5]}"
                         f"\n\nIkkichi telefon raqam: {employee[-2]}"
                         f"\n\nBiriktirilgan sinf: {employee[2]}",
                    reply_markup=await admin_check_btn(
                        user_id=employee[1]
                    )
                )
    else:
        await message.answer(
            text="Hozircha so'rovlar mavjud emas!"
        )


@dp.callback_query_handler(F.data.contains('admincheck_'), state='*')
async def aae_check(call: types.CallbackQuery, state: FSMContext):
    telegram_id = call.data.split('_')[1]

    await db.update_employee_access(
        access=True, telegram_id=telegram_id
    )
    await call.answer(
        text="Hodim ma'lumotlari saqlandi!", show_alert=True
    )
    await call.message.delete()
    await bot.send_message(
        chat_id=telegram_id,
        text="Kiritgan ma'lumotlaringiz bot admini tomonidan tasdiqlandi! /start buyrug'ini qayta kiritib botdan "
             "foydalanishingiz mumkin!"
    )
    await state.finish()


@dp.callback_query_handler(F.data.contains('admincancel_'), state='*')
async def a_e_a_cancel(call: types.CallbackQuery, state: FSMContext):
    telegram_id = call.data.split('_')[1]

    await state.update_data(
        telegram_id=telegram_id
    )
    await call.message.edit_text(
        text="Bekor qilish sababini kiriting:"
    )
    await AdminEducator_State.cancel_message.set()


@dp.message_handler(state=AdminEducator_State.cancel_message)
async def a_e_a_canceltext(message: types.Message, state: FSMContext):
    await state.update_data(
        cancel_text=message.text
    )
    await message.answer(
        text="Habaringizni tasdiqlaysizmi?",
        reply_markup=admin_check_keyboard
    )
    await AdminEducator_State.cancel_check.set()


@dp.callback_query_handler(state=AdminEducator_State.cancel_check)
async def a_e_a_cancelcheck(call: types.CallbackQuery, state: FSMContext):
    if call.data == "canceladmin":
        await call.message.edit_text(
            text="Habaringizni qayta kiriting:"
        )
        await AdminEducator_State.cancel_message.set()

    elif call.data == "send_to_user":
        data = await state.get_data()
        telegram_id = data.get("telegram_id")
        cancel_text = data.get("cancel_text")

        await db.delete_employees(
            telegram_id=telegram_id
        )
        await bot.send_message(
            chat_id=telegram_id,
            text=f"Bot admini tomonidan kiritgan ma'lumotlaringiz qabul qilinmadi!"
                 f"\n\n<b>Sabab: {cancel_text}</b>"
                 f"\n\nIltimos, ma'lumotlaringizni qayta kiriting!"
        )
        await call.message.delete()
        await call.answer(
            text=f"Habar foydalanuvchiga yuborildi!",
            show_alert=True
        )
        await state.finish()
