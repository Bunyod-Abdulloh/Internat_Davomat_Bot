from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.main_menu_cbuttons import main_menu_uz
from keyboards.inline.admin_inline_keys import admin_check_keyboard
from loader import dp, db, bot
from states.admin_state import AdminEducator_State


# a_e_a - Admin educators add (handlers/file_name)


@dp.callback_query_handler(text_contains="admincheck_", state="*")
async def a_e_a_check(call: types.CallbackQuery, state: FSMContext):

    telegram_id = call.data.split('_')[1]

    await db.update_educator_access(
        access=True, telegram_id=telegram_id
    )
    await call.answer(
        text="Hodim ma'lumotlari saqlandi!", show_alert=True
    )
    await call.message.delete()
    await bot.send_message(
        chat_id=telegram_id,
        text="Kiritgan ma'lumotlaringiz bot admini tomonidan tasdiqlandi! /start buyrug'ini qayta kiritib botdan"
             " foydalanishingiz mumkin!"
    )
    await state.finish()


@dp.callback_query_handler(text_contains='admincancel_', state='*')
async def a_e_a_cancel(call: types.CallbackQuery, state: FSMContext):
    telegram_id = call.data.split('_')[1]
    class_number = call.data.split('_')[-1]

    await state.update_data(
        educator_telegram_id=telegram_id,
        educator_class_number=class_number
    )
    await call.message.edit_text(
        text="Bekor qilish sababini kiriting:"
    )
    await AdminEducator_State.cancel_message.set()


@dp.message_handler(state=AdminEducator_State.cancel_message)
async def a_e_a_canceltext(message: types.Message, state: FSMContext):
    await state.update_data(
        educator_cancel_text=message.text
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

    elif call.data == "checkadmin":
        data = await state.get_data()

        telegram_id = data.get("educator_telegram_id")
        cancel_text = data.get("educator_cancel_text")
        class_number = data.get("educator_class_number")
        await db.update_educator_telegram(
            telegram_id=telegram_id, class_number=class_number
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
