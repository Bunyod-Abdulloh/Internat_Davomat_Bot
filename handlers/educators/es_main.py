from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.default.main_menu_cbuttons import main_menu_uz
from keyboards.inline.admin_inline_keys import admin_check_btn
from keyboards.inline.educators_inline_keys import edu_phone_number, educators_class_btn_uz, educators_main_uz
from loader import dp, db, bot
from magic_filter import F
from states.educators_states import EducatorsQuestionnaire, EducatorsMorning, EducatorsDiurnal


# e_m = Educators_main (handlers/educators/file-name)
@dp.message_handler(F.text == '🧑‍🏫 Tarbiyachi', state='*')
async def em_main(message: types.Message):
    educator = await db.select_educator(telegram_id=message.from_user.id)

    if not educator:
        await message.answer(
            text="O'zingizga biriktirilgan sinf yoki sinflarni tanlang:", reply_markup=await educators_class_btn_uz()
        )
        await EducatorsQuestionnaire.select_class.set()
    else:
        current_hour = datetime.now().hour

        morning = [6, 7, 8, 9, 10]
        day = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]

        if current_hour in morning:
            await message.answer(
                text="Tugmalardan birini tanlang:", reply_markup=educators_main_uz
            )
            await EducatorsMorning.main.set()
        elif current_hour in day:
            await message.answer(
                text="Tugmalardan birini tanlang:", reply_markup=educators_main_uz
            )
            await EducatorsDiurnal.main.set()
        else:
            await message.answer(
                text="Ushbu bo'lim faqat ish vaqtida ochiladi!"
            )


@dp.callback_query_handler(state=EducatorsQuestionnaire.select_class)
async def e_m_select_class(call: types.CallbackQuery, state: FSMContext):

    if call.data == "eduback_one":
        await call.message.delete()
        await call.message.answer(
            text="Bosh sahifa", reply_markup=main_menu_uz
        )
        await state.finish()

    elif call.data == "educontinue":
        await call.message.edit_text(
            text="Ism, familiya va otangizni ismini kiriting:\n\n<b>Namuna: Djalilov Zoir Saydirahmon o'g'li</b>"
        )
        await EducatorsQuestionnaire.fullname.set()
    else:
        educator = await db.select_educator_mark(telegram_id=call.from_user.id, class_number=call.data)

        if educator is None:
            await db.add_educator_new(
                telegram_id=call.from_user.id, mark="✅", class_number=call.data
            )
        else:
            if educator[0] == "✅":
                await db.update_educator_telegram(
                    telegram_id=call.from_user.id, mark="🔘", class_number=call.data
                )
            else:
                await db.update_educator_mark(
                    mark="✅", telegram_id=call.from_user.id, class_number=call.data
                )
        await call.message.edit_text(
            text="O'zingizga biriktirilgan sinf yoki sinflarni tanlang:", reply_markup=await educators_class_btn_uz()
        )


@dp.message_handler(state=EducatorsQuestionnaire.fullname)
async def em_get_fullname(message: types.Message):
    await db.update_educator_fullname(
        fullname=message.text, telegram_id=message.from_user.id
    )
    await message.answer(
        text="Telefon raqamingizni kiriting:\n\n<b>Namuna: 998974450292</b>"
    )
    await EducatorsQuestionnaire.first_number.set()


@dp.message_handler(state=EducatorsQuestionnaire.first_number)
async def educators_get_first_number(message: types.Message):
    if message.text.isdigit():
        await db.update_educator_first_phone(first_phone=f"+{message.text}", telegram_id=message.from_user.id)

        await message.answer(
            text="Agar raqamingiz ikkita bo'lsa <b><i>Raqam kiritish</i></b> tugmasini, bitta bo'lsa "
                 "<b><i>Raqamim bitta</i></b> tugmasini bosing!",
            reply_markup=edu_phone_number
        )
        await EducatorsQuestionnaire.second_number.set()
    else:
        await message.answer(
            text="Iltimos faqat raqam kiriting"
        )


@dp.callback_query_handler(state=EducatorsQuestionnaire.second_number)
async def educators_get_second_number(call: types.CallbackQuery):
    if call.data == "add_edusecond_number":
        await call.message.edit_text(
            text="Ikkinchi raqamingizni kiriting:\n\n<b>Namuna: 998974450292</b>"
        )
        await EducatorsQuestionnaire.check_second_number.set()

    elif call.data == "edu_number_first":
        await call.message.edit_text(
            text="Ma'lumotlaringiz qabul qilindi! Admin ma'lumotlaringizni tasdiqlaganidan so'ng botdan "
                 "foydalanishingiz mumkin!"
        )
        await bot.send_message(
            text="Yangi hodim ma'lumotlari qabul qilindi! Ko'rish uchun /new_employee buyrug'ini kiriting!"
        )
        educator = await db.select_educator(telegram_id=call.from_user.id)

        sinf = str()

        for classes in educator:
            sinf += f"{classes[4]} "

        datas = await db.select_educator_distinct(telegram_id=call.from_user.id)

        for admin in ADMINS:
            await bot.send_message(
                chat_id=admin,
                text=f"Yangi hodim ma'lumotlari qabul qilindi!"
                     f"\n\nLavozim: Tarbiyachi"
                     f"\n\nF I SH: {datas[1]}"
                     f"\n\nTelefon raqam: {datas[2]}"
                     f"\n\nSinf: {sinf}",
                reply_markup=await admin_check_btn(
                    user_id=call.from_user.id
                )
            )


@dp.message_handler(state=EducatorsQuestionnaire.check_second_number)
async def educators_check_second_number(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await db.update_educator_second_phone(
            second_phone=f"+{message.text}", telegram_id=message.from_user.id
        )
        await message.answer(
            text="Ma'lumotlaringiz qabul qilindi! Admin ma'lumotlaringizni tasdiqlaganidan so'ng botdan "
                 "foydalanishingiz mumkin!"
        )
        educator = await db.select_educator(telegram_id=message.from_user.id)

        sinf = str()

        for classes in educator:
            sinf += f"{classes[4]} "

        datas = await db.select_educator_distinct(telegram_id=message.from_user.id)

        for admin in ADMINS:
            await bot.send_message(
                chat_id=admin,
                text=f"Yangi hodim ma'lumotlari qabul qilindi!"
                     f"\n\nLavozim: Tarbiyachi"
                     f"\n\nF I SH: {datas[1]}"
                     f"\n\nTelefon raqam: {datas[2]}"
                     f"\n\nIkkinchi telefon raqam: {datas[3]}"
                     f"\n\nSinf: {sinf}",
                reply_markup=await admin_check_btn(
                    user_id=message.from_user.id
                )
            )
    else:
        await message.answer(
            text="Iltimos, faqat raqam kiriting!"
        )
