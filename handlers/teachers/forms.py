from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.default.main_menu_cbuttons import main_menu_uz
from keyboards.inline.all_inline_keys import teachers_multiselect_keyboard
from keyboards.inline.educators_inline_keys import edu_phone_number
from loader import db, dp, bot
from states.teachers_state import TeacherForm


@dp.callback_query_handler(state=TeacherForm.select_class)
async def teachers_select_class_cmd(call: types.CallbackQuery, state: FSMContext):
    telegram_id = call.from_user.id
    if call.data == "eduback_one":
        await call.message.delete()
        await call.message.answer(
            text="Bosh sahifa", reply_markup=main_menu_uz
        )
        await state.finish()
    elif call.data == "educontinue":
        teacher = await db.select_employee(telegram_id=telegram_id, position='Sinf rahbar')
        if teacher:
            await call.message.edit_text(
                text="Ism, familiya va otangizni ismini kiriting:\n\n<b>Namuna: Djalilov Zoir Saydirahmon "
                     "o'g'li</b>"
            )
            await TeacherForm.fullname.set()
        else:
            await call.message.edit_text(
                text="O'zingizga biriktirilgan sinf yoki sinflarni tanlang:",
                reply_markup=await teachers_multiselect_keyboard(telegram_id=telegram_id)
            )
    else:
        level = call.data.split('_')[1]
        user = await db.select_employee_level(telegram_id=telegram_id, level=level, position='Sinf rahbar')
        if user is None:
            await db.add_employee_sql(
                level=level, telegram_id=telegram_id, position='Sinf rahbar'
            )
        else:
            await db.delete_employees_class(
                telegram_id=telegram_id, level=level, position='Sinf rahbar'
            )
        await call.message.edit_text(
            text="O'zingizga biriktirilgan sinf yoki sinflarni tanlang:",
            reply_markup=await teachers_multiselect_keyboard(
                telegram_id=telegram_id, next_step=True
            )
        )


@dp.message_handler(state=TeacherForm.fullname)
async def get_fullname_teachers_cmd(message: types.Message):
    await db.update_employee_fullname(
        fullname=message.text, position="Sinf rahbar", telegram_id=message.from_user.id
    )
    await message.answer(
        text="Telefon raqamingizni kiriting:\n\n<b>Namuna: 998974450292</b>"
    )
    await TeacherForm.first_phone.set()


@dp.message_handler(state=TeacherForm.first_phone)
async def update_first_phone_teachers(message: types.Message):
    if message.text.isdigit():
        await db.update_employee_first_phone(
            first_phone=f"+{message.text}", telegram_id=message.from_user.id, position='Sinf rahbar'
        )
        await message.answer(
            text="Agar raqamingiz ikkita bo'lsa <b><i>Raqam kiritish</i></b> tugmasini, bitta bo'lsa "
                 "<b><i>Raqamim bitta</i></b> tugmasini bosing!",
            reply_markup=edu_phone_number
        )
        await TeacherForm.second_phone.set()
    else:
        await message.answer(
            text="Iltimos faqat raqam kiriting"
        )


@dp.callback_query_handler(state=TeacherForm.second_phone)
async def update_second_phone_teachers(call: types.CallbackQuery, state: FSMContext):
    if call.data == "add_edusecond_number":
        await call.message.edit_text(
            text="Ikkinchi raqamingizni kiriting:\n\n<b>Namuna: 998974450292</b>"
        )
        await TeacherForm.check_second_phone.set()
    elif call.data == "edu_number_first":
        await call.message.edit_text(
            text="Ma'lumotlaringiz qabul qilindi! Admin ma'lumotlaringizni tasdiqlaganidan so'ng botdan "
                 "foydalanishingiz mumkin!"
        )
        await bot.send_message(
            chat_id=ADMINS[0],
            text="Yangi hodim ma'lumotlari qabul qilindi! Ko'rish uchun /new_employee buyrug'ini kiriting!"
        )
        await state.finish()


@dp.message_handler(state=TeacherForm.check_second_phone)
async def educators_check_second_number(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await db.update_employee_second_phone(
            second_phone=f"+{message.text}", telegram_id=message.from_user.id, position='Sinf rahbar'
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
