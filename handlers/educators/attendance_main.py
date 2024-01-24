from datetime import datetime

from aiogram import types
from magic_filter import F

from handlers.a_priority.asd import get_work_time
from keyboards.default.educator_buttons import educators_main_buttons
from keyboards.inline.educators_inline_keys import select_level_educators
from keyboards.inline.student_inline_buttons import view_students_uz
from loader import dp, db
from states.educators_states import EducatorsMorning


@dp.message_handler(F.text == "📊 Davomat kiritish", state="*")
async def es_main_attendance(message: types.Message):
    work_time = await get_work_time(current_hour=datetime.now().hour)
    telegram_id = message.from_user.id
    get_attendance = await db.select_check_work_telegram(telegram_id=telegram_id)
    if work_time == 'morning':
        if get_attendance:
            if len(get_attendance) == 1:
                level = get_attendance[0][1]
                employee_attendance = await db.select_check_work(telegram_id=telegram_id, level=level)
                if employee_attendance[1] is True:
                    await message.answer(
                        text=f"Siz {level} sinfini yo'qlama qilib bo'lgansiz!"
                    )
                else:
                    current_date = datetime.now().date()
                    get_morning = await db.get_morning(level=level)
                    await message.answer(
                        text=f"Sana: {current_date}\nSinf: {level}\nJami o'quvchilar soni: {len(get_morning)} ta "
                             f"\n\nO'quvchilarni kelgan kelmaganligini tugmalarni bosib belgilang va yakunda "
                             f"<b>☑️ Tasdiqlash</b> tugmasini bosing!"
                             f"\n\n✅ - Kelganlar\n☑️ - Sababli kelmaganlar\n❎ - Sababsiz kelmaganlar",
                        reply_markup=await view_students_uz(
                            work_time=get_morning, level=level, morning=True)
                    )
                    await EducatorsMorning.attendance.set()
            else:
                await message.answer(
                    text="Sinflardan birini tanlang:",
                    reply_markup=await select_level_educators(telegram_id=telegram_id)
                )
                await EducatorsMorning.first_class.set()
        else:
            await message.answer(
                text="Avval ✅ Ishga keldim! tugmasini bosib kerakli bo'limni tanlang!"
            )
    elif work_time == 'day':
        pass
    else:
        await message.answer(
            text='Ushbu bo\'lim faqat ish vaqtida ishlaydi!'
        )


@dp.callback_query_handler(state=EducatorsMorning.first_class)
async def ma_first_class(call: types.CallbackQuery):
    telegram_id = call.from_user.id
    if call.data == "back":
        await call.message.answer(
            text="Tarbiyachi bo'limi", reply_markup=educators_main_buttons()
        )
        await call.message.delete()
    else:
        level = call.data
        employee_attendance = await db.select_check_work(telegram_id=telegram_id, level=level)
        if employee_attendance[1] is True:
            await call.answer(
                text=f"Siz {level} sinfini yo'qlama qilib bo'lgansiz!", show_alert=True
            )
        else:
            current_date = datetime.now().date()
            get_morning = await db.get_morning(
                level=level
            )
            await call.message.edit_text(
                text=f"Sana: {current_date}\nSinf: {level}\nJami o'quvchilar soni: {len(get_morning)} ta "
                     f"\n\nO'quvchilarni kelgan kelmaganligini tugmalarni bosib belgilang va yakunda "
                     f"<b>☑️ Tasdiqlash</b> tugmasini bosing!"
                     f"\n\n✅ - Kelganlar\n☑️ - Sababli kelmaganlar\n❎ - Sababsiz kelmaganlar",
                reply_markup=await view_students_uz(
                    work_time=get_morning, level=level, morning=True)
            )
            await EducatorsMorning.attendance.set()
