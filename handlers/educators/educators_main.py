from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.inline.admin_inline_keys import admin_check_button, educators_class_button
from keyboards.inline.all_inline_keys import classes_list
from keyboards.inline.educators_inline_keys import edu_phone_number, edu_work_time
from loader import dp, db, bot
from states.educators_states import Educators_State


@dp.callback_query_handler(text='educator', state='*')
async def educators_first_main(call: types.CallbackQuery):
    await call.message.edit_text(
        text="O'zingizga biriktirilgan sinfni tanlang:",
        reply_markup=await educators_class_button()
    )
    await Educators_State.select_class.set()


@dp.callback_query_handler(text="edu_back", state="*")
async def e_m_back(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        text="Tarbiyachilar bo'limi", reply_markup=await educators_class_button()
    )
    await state.finish()


@dp.callback_query_handler(state=Educators_State.select_class)
async def educators_select_class(call: types.CallbackQuery, state: FSMContext):
    select_educator = await db.select_educator_(telegram_id=call.from_user.id, class_number=call.data)

    if not select_educator:
        await db.add_educator_(
            telegram_id=call.from_user.id, class_number=call.data
        )
        await state.update_data(
            educator_class_number=call.data
        )
        await call.message.edit_text(
            text="Ism, familiya va otangizni ismini kiriting:"
                 "\n\n<b>Namuna: Djalilov Zoir Saydirahmon o'g'li</b>"
        )
        await Educators_State.fullname.set()
    else:
        if select_educator[-1] is False:
            await call.answer(
                text="Ma'lumotlaringiz hali admin tomonidan tasdiqlanmadi!", show_alert=True
            )
        else:
            await call.message.edit_text(
                text="Ish vaqtingizni tanlang:", reply_markup=edu_work_time
            )


@dp.message_handler(state=Educators_State.fullname)
async def educators_get_fullname(message: types.Message, state: FSMContext):
    data = await state.get_data()
    class_number = data['educator_class_number']
    await db.update_educator_fullname(
        fullname=message.text, telegram_id=message.from_user.id, class_number=class_number
    )
    await message.answer(
        text="Telefon raqamingizni kiriting:\n\n<b>Namuna: 998974450292</b>"
    )
    await Educators_State.first_number.set()


@dp.message_handler(state=Educators_State.first_number)
async def educators_get_first_number(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await db.update_educator_first_phone(first_phone=f"+{message.text}", telegram_id=message.from_user.id)

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
            text="Ikkinchi raqamingizni kiriting:\n\n<b>Namuna: 998974450292</b>"
        )
        await Educators_State.check_second_number.set()

    elif call.data == "edu_number_first":
        await call.message.edit_text(
            text="Ma'lumotlaringiz qabul qilindi! Admin ma'lumotlaringizni tasdiqlaganidan so'ng botdan "
                 "foydalanishingiz mumkin!"
        )
        data = await state.get_data()
        class_number = data.get('educator_class_number')
        educator = await db.select_educator_(telegram_id=call.from_user.id, class_number=class_number)

        for admin in ADMINS:
            await bot.send_message(
                chat_id=admin,
                text=f"Yangi hodim ma'lumotlari qabul qilindi!"
                     f"\n\nLavozimi: Tarbiyachi"
                     f"\n\nF.I.Sh: {educator[1]}"
                     f"\n\nTelefon raqami: {educator[2]}"
                     f"\n\nSinfi: {educator[4]}",
                reply_markup=await admin_check_button(
                    user_id=call.from_user.id,
                    class_number=educator[4]
                )
            )
        await state.finish()


@dp.message_handler(state=Educators_State.check_second_number)
async def educators_check_second_number(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await db.update_educator_second_phone(
            second_phone=f"+{message.text}", telegram_id=message.from_user.id
        )

        await message.answer(
            text="Ma'lumotlaringiz qabul qilindi! Admin ma'lumotlaringizni tasdiqlaganidan so'ng botdan "
                 "foydalanishingiz mumkin!"
        )
        data = await state.get_data()
        class_number = data.get('class_number')
        educator = await db.select_educator_(telegram_id=message.from_user.id, class_number=class_number)

        for admin in ADMINS:
            await bot.send_message(
                chat_id=admin,
                text=f"Yangi hodim ma'lumotlari qabul qilindi!"
                     f"\n\nLavozimi: Tarbiyachi"
                     f"\n\nF.I.Sh: {educator[1]}"
                     f"\n\nTelefon raqami: {educator[2]}"
                     f"\n\nIkkinchi telefon raqami: {educator[3]}"
                     f"\n\nSinfi: {educator[4]}",
                reply_markup=await admin_check_button(
                    user_id=message.from_user.id
                )
            )
    else:
        await message.answer(
            text="Iltimos, faqat raqam kiriting!"
        )
