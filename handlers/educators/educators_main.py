from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.inline.admin_inline_keys import admin_check_button
from keyboards.inline.educators_inline_keys import edu_phone_number
from loader import dp, db, bot
from states.educators_states import Educators_State


@dp.callback_query_handler(text='educator', state='*')
async def educators_first_main(call: types.CallbackQuery):
    educator = await db.select_educator(
        telegram_id=call.from_user.id
    )

    if not educator:
        await call.message.edit_text(
            text="Ismingizni kiriting:"
        )
        await Educators_State.firstname.set()
    else:
        pass


@dp.message_handler(state=Educators_State.firstname)
async def educators_get_firstname(message: types.Message, state: FSMContext):
    if message.text.isalpha():
        await state.update_data(
            educator_first_name=message.text
        )
        await message.answer(
            text="Familiyangizni kiriting:"
        )
        await Educators_State.lastname.set()
    else:
        await message.answer(
            text="Iltimos faqat harf kiriting!"
        )


@dp.message_handler(state=Educators_State.lastname)
async def educators_get_lastname(message: types.Message, state: FSMContext):
    if message.text.isalpha():
        await state.update_data(
            educator_last_name=message.text
        )
        await message.answer(
            text="Otangizni ismini kiriting:"
        )
        await Educators_State.surname.set()
    else:
        await message.answer(
            text="Iltimos faqat harf kiriting"
        )


@dp.message_handler(state=Educators_State.surname)
async def educators_get_surname(message: types.Message, state: FSMContext):
    if message.text.isalpha():
        await state.update_data(
            educator_surname=message.text
        )
        await message.answer(
            text="Telefon raqamingizni kiriting:"
                 "\n\n<b>Namuna: 998974450292</b>"
        )
        await Educators_State.first_number.set()
    else:
        await message.answer(
            text="Iltimos faqat harf kiriting"
        )


@dp.message_handler(state=Educators_State.first_number)
async def educators_get_first_number(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(
            educator_first_number=f"+{message.text}"
        )
        await message.answer(
            text="Agar raqamingiz ikkita bo'lsa <b><i>Raqam kiritish</i></b> tugmasini, bitta bo'lsa "
                 "<b><i>Raqamim bitta</i></b> tugmasini bosing!",
            reply_markup=edu_phone_number
        )
        await Educators_State.second_number.set()
    else:
        await message.answer(
            text="Iltimos faqat raqam kiriting"
        )


@dp.callback_query_handler(state=Educators_State.second_number)
async def educators_get_second_number(call: types.CallbackQuery, state: FSMContext):
    if call.data == "add_edusecond_number":
        await call.message.edit_text(
            text="Ikkinchi raqamingizni kiriting:"
                 "\n\n<b>Namuna: 998974450292</b>"
        )
        await Educators_State.check_second_number.set()

    elif call.data == "edu_number_first":
        await call.message.edit_text(
            text="Ish kunlaringizni kiriting:"
                 "\n\n<b>Namuna: Dushanba, Chorshanba, Juma</b>"
        )
        await Educators_State.work_days.set()


@dp.message_handler(state=Educators_State.check_second_number)
async def educators_check_second_number(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(
            educator_second_number=f"+{message.text}"
        )
        await message.answer(
            text="Ish kunlaringizni kiriting:"
                 "\n\n<b>Namuna: Dushanba, Chorshanba, Juma</b>"
        )
        await Educators_State.work_days.set()

    else:
        await message.answer(
            text="Iltimos, faqat raqam kiriting:"
        )


@dp.message_handler(state=Educators_State.work_days)
async def educators_get_work_days(message: types.Message, state: FSMContext):
    await state.update_data(
        educator_work_days=message.text
    )
    await message.answer(
        text="Ma'lumotlaringiz qabul qilindi! Admin ma'lumotlaringizni tasdiqlaganidan so'ng botdan "
             "foydalanishingiz mumkin!"
    )
    data = await state.get_data()
    first_name = data['educator_first_name']
    last_name = data['educator_last_name']
    surname = data['educator_surname']
    first_number = data['educator_first_number']
    work_days = data['educator_work_days']

    for admin in ADMINS:
        if 'educator_second_number' in data.keys():
            await bot.send_message(
                chat_id=admin,
                text=f"Yangi tarbiyachi ma'lumotlari qabul qilindi!"
                     f"\n\nIsmi: {first_name}"
                     f"\nFamiliyasi: {last_name}"
                     f"\nOtasining ismi: {surname}"
                     f"\nTelefon raqami: {first_number}"
                     f"\nIkkinchi telefon raqami: {data['educator_second_number']}"
                     f"\nIsh kunlari: {work_days}",
                reply_markup=admin_check_button(
                    user_id=message.from_user.id
                )
            )
        else:
            await bot.send_message(
                chat_id=admin,
                text=f"Yangi tarbiyachi ma'lumotlari qabul qilindi!"
                     f"\n\nIsmi: {first_name}"
                     f"\nFamiliyasi: {last_name}"
                     f"\nOtasining ismi: {surname}"
                     f"\nTelefon raqami: {first_number}"
                     f"\nIsh kunlari: {work_days}",
                reply_markup=admin_check_button(
                    user_id=message.from_user.id
                )
            )
