from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, db, bot


@dp.callback_query_handler(text_contains='', state='*')
async def admin_educators_check(call: types.CallbackQuery, state: FSMContext):
    user_id = call.data.split('_')[-1]

    data = await state.get_data()
    first_name = data['educator_first_name']
    last_name = data['educator_last_name']
    surname = data['educator_surname']
    first_number = data['educator_first_number']
    work_days = data['educator_work_days']

    if 'educator_second_number' in data.keys():
        await db.add_educators(
            firstname=first_name,
            lastname=last_name,
            surname=surname,
            first_number=first_number,
            second_number=data['educator_second_number'],
            work_days=work_days,
            telegram_id=user_id
        )
    else:
        await db.add_educators(
            firstname=first_name,
            lastname=last_name,
            surname=surname,
            first_number=first_number,
            work_days=work_days,
            telegram_id=user_id
        )

    await call.message.edit_text(
        text=f"Tarbiyachi {first_name, last_name, surname}ning ma'lumotlari saqlandi!"
    )

    await bot.send_message(
        chat_id=user_id,
        text="Ma'lumotlaringiz bot admini tomonidan tasdiqlandi! Botdan foydalanishingiz mumkin!"
    )
