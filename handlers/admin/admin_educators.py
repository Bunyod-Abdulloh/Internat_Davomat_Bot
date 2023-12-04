from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.admin_inline_keys import admin_check_keyboard
from loader import dp, db, bot
from states.admin_state import AdminEducator_State


@dp.callback_query_handler(text_contains="admincheck_", state="*")
async def admin_educators_check(call: types.CallbackQuery, state: FSMContext):
    try:
        user_id = call.data.split('_')[-1]

        data = await state.get_data()
        print(data)
        fullname = data['educator_fullname']
        first_number = data['educator_first_number']
        class_number = data['educator_class_number']

        if 'educator_second_number' in data.keys():
            await db.add_educators(
                fullname=fullname,
                first_number=first_number,
                second_number=data['educator_second_number'],
                class_number=class_number,
                telegram_id=user_id
            )
        else:
            await db.add_educators(
                fullname=fullname,
                first_number=first_number,
                class_number=class_number,
                telegram_id=user_id
            )

        await call.message.edit_text(
            text=f"Tarbiyachi {fullname}ning ma'lumotlari saqlandi!"
        )

        await bot.send_message(
            chat_id=user_id,
            text="Ma'lumotlaringiz bot admini tomonidan tasdiqlandi! Botdan foydalanishingiz mumkin!"
        )
        await state.finish()
    except Exception as err:
        print(f"{err} admin edu 46")


@dp.callback_query_handler(text_contains='admincancel_', state='*')
async def admin_educators_cancel(call: types.CallbackQuery, state: FSMContext):
    educator_id = call.data.split('_')[-1]
    await state.update_data(
        educator_id=educator_id
    )
    await call.message.edit_text(
        text="Bekor qilish sababini kiriting:"
    )
    await AdminEducator_State.cancel_message.set()


@dp.message_handler(state=AdminEducator_State.cancel_message)
async def admin_educator_canceltext(message: types.Message, state: FSMContext):
    await state.update_data(
        cancel_text=message.text
    )
    await message.answer(
        text="Habaringizni tasdiqlaysizmi?",
        reply_markup=admin_check_keyboard
    )
    await AdminEducator_State.cancel_check.set()


@dp.callback_query_handler(state=AdminEducator_State.cancel_check)
async def admin_educator_cancelcheck(call: types.CallbackQuery, state: FSMContext):
    if call.data == "canceladmin":
        await call.message.edit_text(
            text="Habaringizni qayta kiriting:"
        )
        await AdminEducator_State.cancel_message.set()

    elif call.data == "checkadmin":
        data = await state.get_data()
        educator_id = data["educator_id"]
        fullname = data['educator_fullname']
        cancel_text = data["cancel_text"]

        await bot.send_message(
            chat_id=educator_id,
            text=f"Bot admini tomonidan kiritgan ma'lumotlaringiz qabul qilinmadi!"
                 f"\nIltimos, ma'lumotlaringizni qayta kiriting!"
                 f"\n\n<b>Sabab: {cancel_text}</b>"
        )
        await call.answer(
            text=f"Habar foydalanuvchi {fullname}ga yuborildi!"
        )
        await state.finish()
