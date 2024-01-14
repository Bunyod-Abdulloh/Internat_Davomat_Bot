from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default.main_menu_cbuttons import main_menu_uz
from keyboards.inline.all_inline_keys import generate_multiselect_keyboard
from keyboards.inline.educators_inline_keys import edu_phone_number, educators_main_uz
from states.educators_states import EducatorsQuestionnaire, EducatorsMorning, EducatorsDiurnal
from magic_filter import F
from data.config import ADMINS
from loader import dp, db, bot


# e_m = Educators_main (handlers/educators/file-name)
@dp.message_handler(F.text == '🧑‍🏫 Tarbiyachi', state='*')
async def em_main(message: types.Message):
    telegram_id = message.from_user.id
    educator = await db.select_employee(telegram_id=telegram_id)
    classes = await db.select_all_classes()

    if not educator:
        await message.answer(
            text="O'zingizga biriktirilgan sinf yoki sinflarni tanlang:",
            reply_markup=await generate_multiselect_keyboard(telegram_id=telegram_id, table_from_db=classes)
        )
        await EducatorsQuestionnaire.select_class.set()
    else:
        if educator[0][-1] is False:
            await db.delete_employees(
                telegram_id=message.from_user.id
            )
            await message.answer(
                text="Ma'lumotlaringiz tasdiqlanmadi! \nIltimos ma'lumotlaringizni qayta kiriting!"
                     "\n\nO'zingizga biriktirilgan sinf yoki sinflarni tanlang:",
                reply_markup=await generate_multiselect_keyboard(telegram_id=telegram_id, table_from_db=classes)
            )
            await db.delete_employees(
                telegram_id=message.from_user.id
            )
            await EducatorsQuestionnaire.select_class.set()
        else:
            current_hour = datetime.now().hour

            morning = [6, 7, 8, 9, 10]
            day = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]

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
    telegram_id = call.from_user.id
    classes = await db.select_all_classes()

    if call.data == "eduback_one":
        await call.message.delete()
        await call.message.answer(
            text="Bosh sahifa", reply_markup=main_menu_uz
        )
        await state.finish()
    elif call.data == "educontinue":
        educator = await db.select_employee(telegram_id=telegram_id)
        if educator:
            await call.message.edit_text(
                text="Ism, familiya va otangizni ismini kiriting:\n\n<b>Namuna: Djalilov Zoir Saydirahmon "
                     "o'g'li</b>"
            )
            await EducatorsQuestionnaire.fullname.set()
        else:
            await call.message.edit_text(
                text="O'zingizga biriktirilgan sinf yoki sinflarni tanlang:",
                reply_markup=await generate_multiselect_keyboard(telegram_id=telegram_id, table_from_db=classes)
            )
            await EducatorsQuestionnaire.select_class.set()

    else:
        level = call.data.split('_')[1]
        user = await db.select_employee(telegram_id=telegram_id, level=level)

        if not user:
            await db.add_employee(
                telegram_id=telegram_id, level=level
            )
        else:
            await db.delete_employees_class(
                telegram_id=telegram_id, level=level
            )
        await call.message.edit_text(
            text="O'zingizga biriktirilgan sinf yoki sinflarni tanlang:",
            reply_markup=await generate_multiselect_keyboard(
                telegram_id=telegram_id, table_from_db=classes, next_step=True
            )
        )


@dp.message_handler(state=EducatorsQuestionnaire.fullname)
async def em_get_fullname(message: types.Message):
    await db.update_employee_fullname(
        fullname=message.text, position="Tarbiyachi", telegram_id=message.from_user.id
    )
    await message.answer(
        text="Telefon raqamingizni kiriting:\n\n<b>Namuna: 998974450292</b>"
    )
    await EducatorsQuestionnaire.first_number.set()


@dp.message_handler(state=EducatorsQuestionnaire.first_number)
async def educators_get_first_number(message: types.Message):
    if message.text.isdigit():
        await db.update_employee_first_phone(
            first_phone=f"+{message.text}",
            telegram_id=message.from_user.id
        )
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
async def educators_get_second_number(call: types.CallbackQuery, state: FSMContext):
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
            chat_id=ADMINS[0],
            text="Yangi hodim ma'lumotlari qabul qilindi! Ko'rish uchun /new_employees buyrug'ini kiriting!"
        )
        await state.finish()


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
        await bot.send_message(
            chat_id=ADMINS[0],
            text="Yangi hodim ma'lumotlari qabul qilindi! Ko'rish uchun /new_employee buyrug'ini kiriting!"
        )
        await state.finish()

    else:
        await message.answer(
            text="Iltimos, faqat raqam kiriting!"
        )
