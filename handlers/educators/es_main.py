from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from handlers.a_priority.asd import get_work_time
from keyboards.default.educator_buttons import educators_main_buttons
from keyboards.default.main_menu_cbuttons import main_menu_uz
from keyboards.inline.all_inline_keys import generate_multiselect_keyboard
from keyboards.inline.educators_inline_keys import edu_phone_number, check_work_button
from states.educators_states import EducatorForm, EducatorsMorning
from magic_filter import F
from data.config import ADMINS
from loader import dp, db, bot


# e_m = Educators_main (handlers/educators/file-name)
@dp.message_handler(F.text == '🧑‍🏫 Tarbiyachi', state='*')
async def em_main(message: types.Message):
    telegram_id = message.from_user.id
    educator = await db.select_employee_position(telegram_id=telegram_id, position='Tarbiyachi')
    if not educator:
        await message.answer(
            text=message.text, reply_markup=ReplyKeyboardRemove()
        )
        await db.add_employee_sql(
            telegram_id=telegram_id, position='Tarbiyachi'
        )
        await message.answer(
            text="O'zingizga biriktirilgan sinf yoki sinflarni tanlang:",
            reply_markup=await generate_multiselect_keyboard(telegram_id=telegram_id)
        )
        await EducatorForm.select_class.set()
    else:
        if educator[0] is False:
            await db.delete_employees(
                telegram_id=telegram_id, position='Tarbiyachi'
            )
            await message.answer(
                text="Ma'lumotlaringiz tasdiqlanmadi! \nIltimos ma'lumotlaringizni qayta kiriting!"
                     "\n\nO'zingizga biriktirilgan sinf yoki sinflarni tanlang:",
                reply_markup=await generate_multiselect_keyboard(telegram_id=telegram_id)
            )
            await db.delete_employees(
                telegram_id=telegram_id, position='Tarbiyachi'
            )
            await EducatorForm.select_class.set()
        else:
            work_time = await get_work_time(current_hour=datetime.now().hour)
            if work_time == 'morning':
                await message.answer(
                    text="Assalomu alaykum! Internatimizga xush kelibsiz!"
                         "\n\nQuyidagi tugmalardan birini tanlang:",
                    reply_markup=educators_main_buttons()
                )
                await EducatorsMorning.main.set()
            elif work_time == 'day':
                pass
            else:
                await message.answer(
                    text="Ushbu bo'lim faqat ish vaqtida ochiladi!"
                )


@dp.callback_query_handler(state=EducatorForm.select_class)
async def e_m_select_class(call: types.CallbackQuery, state: FSMContext):
    telegram_id = call.from_user.id
    if call.data == "eduback_one":
        await call.message.delete()
        await call.message.answer(
            text="Bosh sahifa", reply_markup=main_menu_uz
        )
        await state.finish()
    elif call.data == "educontinue":
        educator = await db.select_employee(telegram_id=telegram_id, position='Tarbiyachi')
        if educator:
            await call.message.edit_text(
                text="Ism, familiya va otangizni ismini kiriting:\n\n<b>Namuna: Djalilov Zoir Saydirahmon "
                     "o'g'li</b>"
            )
            await EducatorForm.fullname.set()
        else:
            await call.message.edit_text(
                text="O'zingizga biriktirilgan sinf yoki sinflarni tanlang:",
                reply_markup=await generate_multiselect_keyboard(telegram_id=telegram_id)
            )
            await EducatorForm.select_class.set()
    else:
        level = call.data.split('_')[1]
        user = await db.select_employee_level(telegram_id=telegram_id, level=level, position='Tarbiyachi')
        if user is None:
            await db.update_employee_level(
                level=level, position='Tarbiyachi', telegram_id=telegram_id
            )
        else:
            await db.delete_employees_class(
                telegram_id=telegram_id, level=level, position='Tarbiyachi'
            )
        await call.message.edit_text(
            text="O'zingizga biriktirilgan sinf yoki sinflarni tanlang:",
            reply_markup=await generate_multiselect_keyboard(
                telegram_id=telegram_id, next_step=True
            )
        )


@dp.message_handler(state=EducatorForm.fullname)
async def em_get_fullname(message: types.Message):
    await db.update_employee_fullname(
        fullname=message.text, position="Tarbiyachi", telegram_id=message.from_user.id
    )
    await message.answer(
        text="Telefon raqamingizni kiriting:\n\n<b>Namuna: 998974450292</b>"
    )
    await EducatorForm.first_number.set()


@dp.message_handler(state=EducatorForm.first_number)
async def educators_get_first_number(message: types.Message):
    if message.text.isdigit():
        await db.update_employee_first_phone(
            first_phone=f"+{message.text}", telegram_id=message.from_user.id, position='Tarbiyachi'
        )
        await message.answer(
            text="Agar raqamingiz ikkita bo'lsa <b><i>Raqam kiritish</i></b> tugmasini, bitta bo'lsa "
                 "<b><i>Raqamim bitta</i></b> tugmasini bosing!",
            reply_markup=edu_phone_number
        )
        await EducatorForm.second_number.set()
    else:
        await message.answer(
            text="Iltimos faqat raqam kiriting"
        )


@dp.callback_query_handler(state=EducatorForm.second_number)
async def educators_get_second_number(call: types.CallbackQuery, state: FSMContext):
    if call.data == "add_edusecond_number":
        await call.message.edit_text(
            text="Ikkinchi raqamingizni kiriting:\n\n<b>Namuna: 998974450292</b>"
        )
        await EducatorForm.check_second_number.set()

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


@dp.message_handler(state=EducatorForm.check_second_number)
async def educators_check_second_number(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await db.update_employee_second_phone(
            second_phone=f"+{message.text}", telegram_id=message.from_user.id, position='Tarbiyachi'
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


@dp.message_handler(F.text == '✅ Ishga keldim!', state='*')
async def mm_morning_main(message: types.Message):
    work_time = await get_work_time(current_hour=datetime.now().hour)
    if work_time == "morning":
        await message.answer(
            text="Quyidagi tugmalardan birini tanlang:",
            reply_markup=check_work_button()
        )
        await EducatorsMorning.main.set()
    elif work_time == "day":
        pass
    else:
        await message.answer(
            text='Ushbu bo\'lim faqat ish vaqtida ishlaydi!'
        )
