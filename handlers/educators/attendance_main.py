from datetime import datetime

from aiogram import types
from magic_filter import F

from keyboards.inline.educators_inline_keys import select_level_educators
from keyboards.inline.student_inline_buttons import view_students_uz
from loader import dp, db
from states.educators_states import EducatorsMorning


@dp.message_handler(F.text == "📊 Davomat kiritish", state="*")
async def es_main_attendance(message: types.Message):
    current_hour = datetime.now().hour
    day = [6, 7, 8, 9, 10, 11, 12]
    morning = [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    telegram_id = message.from_user.id
    classes = await db.select_employee_return_list(telegram_id=telegram_id)
    attendance = await db.get_educator_morning(educator_id=classes[0][1])

    if current_hour in morning:
        if len(classes) == 1:
            educator = await db.select_employee(
                telegram_id=telegram_id
            )
            level = educator[0]
            get_morning = await db.get_morning(
                level=level
            )
            await message.answer(
                text="O'quvchilarni kelgan kelmaganligini tugmalarni bosib belgilang va yakunda <b>☑️ Tasdiqlash</b> "
                     "tugmasini bosing!"
                     "\n\n✅ - Kelganlar\n\n☑️ - Sababli kelmaganlar\n\n❎ - Sababsiz kelmaganlar",
                reply_markup=await view_students_uz(
                    work_time=get_morning, level=level, morning=True)
            )
            await EducatorsMorning.attendance.set()
        else:
            await message.answer(
                text="Sinflardan birini tanlang:",
                reply_markup=await select_level_educators(
                    classes=classes
                )
            )
            await EducatorsMorning.first_class.set()
    elif current_hour in day:
        pass
