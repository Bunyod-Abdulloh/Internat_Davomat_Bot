from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.admin_inline_keys import admin_check_keyboard
from keyboards.inline.main_menu_inline_keys import main_menu_keys
from loader import dp, db, bot
from states.admin_state import AdminEducator_State


# a_e_a - Admin educators add (handlers/file_name)


@dp.callback_query_handler(text_contains="admincheck_", state="*")
async def a_e_a_check(call: types.CallbackQuery, state: FSMContext):

    telegram_id = call.data.split('_')[-1]

    await db.update_educator_access(
        access=True, telegram_id=telegram_id
    )
    await call.message.edit_text(
        text="Bosh sahifa", reply_markup=main_menu_keys
    )
    await call.answer(
        text="Hodim ma'lumotlari saqlandi!", show_alert=True
    )
    await bot.send_message(
        chat_id=telegram_id, text="Kiritgan ma'lumotlaringiz bot admini tomonidan tasdiqlandi! Botning to'liq "
                                  "imkoniyatlaridan foydalanishingiz mumkin!"
    )
    await state.finish()


@dp.callback_query_handler(text_contains='admincancel_', state='*')
async def a_e_a_cancel(call: types.CallbackQuery, state: FSMContext):
    telegram_id = call.data.split('_')[-1]
    await state.update_data(
        educator_telegram_id=telegram_id
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

    elif call.data == "checkadmin":
        data = await state.get_data()
        educator_telegram_id = data["educator_telegram_id"]
        cancel_text = data["cancel_text"]
        educator = await db.select_educator_(
            telegram_id=educator_telegram_id
        )
        print(educator)

        await bot.send_message(
            chat_id=educator_telegram_id,
            text=f"Bot admini tomonidan kiritgan ma'lumotlaringiz qabul qilinmadi!"
                 f"\nIltimos, ma'lumotlaringizni qayta kiriting!"
                 f"\n\n<b>Sabab: {cancel_text}</b>"
        )
        await call.answer(
            text=f"Habar foydalanuvchiga yuborildi!",
            show_alert=True
        )
        await state.finish()
