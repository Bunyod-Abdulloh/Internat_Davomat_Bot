from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.inline.admin_inline_keys import admin_check_button
from keyboards.inline.all_inline_keys import classes_button, classes_list
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
            text="Ism, familiya va otangizni ismini kiriting:"
                 "\n\n<b>Namuna: Djalilov Zoir Saydirahmon o'g'li</b>"
        )
        await Educators_State.fullname.set()
    else:
        pass


@dp.message_handler(state=Educators_State.fullname)
async def educators_get_firstname(message: types.Message, state: FSMContext):

    await state.update_data(
        educator_fullname=message.text
    )
    await message.answer(
        text="Telefon raqamingizni kiriting:"
             "\n\n<b>Namuna: 998974450292</b>"
    )
    await Educators_State.first_number.set()


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
            text="O'zingizga biriktirilgan sinfni tanlang:",
            reply_markup=classes_button
        )
        await Educators_State.select_class.set()


@dp.callback_query_handler(state=Educators_State.select_class)
async def educators_select_class(call: types.CallbackQuery, state: FSMContext):

    if call.data in classes_list:
        await state.update_data(
            educator_class_number=call.data,
            educator_post="Tarbiyachi"
        )

        await call.message.edit_text(
            text="Ma'lumotlaringiz qabul qilindi! Admin ma'lumotlaringizni tasdiqlaganidan so'ng botdan "
                 "foydalanishingiz mumkin!"
        )
        data = await state.get_data()
        fullname = data['educator_fullname']
        first_number = data['educator_first_number']
        class_number = call.data

        for admin in ADMINS:
            if 'educator_second_number' in data.keys():
                await bot.send_message(
                    chat_id=admin,
                    text=f"Yangi hodim ma'lumotlari qabul qilindi!"
                         f"\n\nLavozimi: Tarbiyachi"
                         f"\n\nF.I.Sh: {fullname}"
                         f"\n\nTelefon raqami: {first_number}"
                         f"\n\nIkkinchi telefon raqami: {data['educator_second_number']}"
                         f"\n\nSinfi: {class_number}",
                    reply_markup=await admin_check_button(
                        user_id=call.from_user.id
                    )
                )
            else:
                await bot.send_message(
                    chat_id=admin,
                    text=f"Yangi hodim ma'lumotlari qabul qilindi!"
                         f"\n\nLavozimi: Tarbiyachi"
                         f"\n\nF.I.Sh: {fullname}"
                         f"\n\nTelefon raqami: {first_number}"
                         f"\n\nSinfi: {class_number}",
                    reply_markup=await admin_check_button(
                        user_id=call.from_user.id
                    )
                )
            await state.reset_state(with_data=False)

    elif call.data == "back_for_classes":
        await call.message.edit_text(
            text="Agar raqamingiz ikkita bo'lsa <b><i>Raqam kiritish</i></b> tugmasini, bitta bo'lsa "
                 "<b><i>Raqamim bitta</i></b> tugmasini bosing!",
            reply_markup=edu_phone_number
        )
        await Educators_State.second_number.set()


@dp.message_handler(state=Educators_State.check_second_number)
async def educators_check_second_number(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(
            educator_second_number=f"+{message.text}"
        )
        await message.answer(
            text="O'zingizga biriktirilgan sinfni tanlang:",
            reply_markup=classes_button
        )
        await Educators_State.select_class.set()
    else:
        await message.answer(
            text="Iltimos, faqat raqam kiriting!"
        )
