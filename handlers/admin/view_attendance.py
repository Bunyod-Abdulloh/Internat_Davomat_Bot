from datetime import datetime

from aiogram import types
from magic_filter import F

from keyboards.default.admin_custom_buttons import admin_attendance_cbuttons
from loader import dp, db


@dp.message_handler(F.text == 'Davomat', state='*')
async def view_attendance_main(message: types. Message):
    await message.answer(
        text='Kerakli bo\'limni tanlang:', reply_markup=admin_attendance_cbuttons
    )


@dp.message_handler(F.text == 'Sinflar davomati', state='*')
async def view_levels_attendance(message: types.Message):
    current_date = datetime.now().date()
    all_levels = await db.select_all_classes()
    submitted = 'Davomat topshirgan sinflar:\n\n'
    not_submitted = '\nDavomat topshirmagan sinflar:\n\n'

    for level in all_levels:
        level_ = f'{level[0]}-{level[1]}'
        check_level = await db.select_check_work_teacher(checked_date=current_date, level=level_)
        if check_level is None:
            not_submitted += f'{level_}\n'
        else:
            submitted += f'{level_}\n'
    await message.answer(
        text=submitted + not_submitted
    )


@dp.message_handler(F.text == 'Kunlik davomat', state='*')
async def view_everydays_attendance(message: types.Message):
    current_date = datetime.now().date()
    all_levels = await db.get_level_attendance(checked_date=current_date)
    all_students = str()
    present = str()
    absent = str()
    explicable = str()
    dormitory = str()
    first_four_present = await db.morning_report(
        first_value=1, second_value=4, check_teacher='✅', current_date=current_date
    )
    one_four_absent = await db.morning_report(
        first_value=1, second_value=4, check_teacher='☑️', current_date=current_date
    )
    one_four_explicable = await db.morning_report(
        first_value=1, second_value=4, check_teacher='❎', current_date=current_date
    )
    five_seven_present = await db.morning_report(
        first_value=5, second_value=7, check_teacher='✅', current_date=current_date
    )
    five_seven_absent = await db.morning_report(
        first_value=5, second_value=7, check_teacher='☑️', current_date=current_date
    )
    five_seven_explicable = await db.morning_report(
        first_value=5, second_value=7, check_teacher='❎', current_date=current_date
    )
    one_seven_present = await db.morning_report(
        first_value=1, second_value=7, check_teacher='✅', current_date=current_date
    )
    one_seven_absent = await db.morning_report(
        first_value=1, second_value=7, check_teacher='☑️', current_date=current_date
    )
    one_seven_explicable = await db.morning_report(
        first_value=1, second_value=7, check_teacher='❎', current_date=current_date
    )
    eight_eleven_present = await db.morning_report(
        first_value=8, second_value=11, check_teacher='✅', current_date=current_date
    )
    eight_eleven_absent = await db.morning_report(
        first_value=8, second_value=11, check_teacher='☑️', current_date=current_date
    )
    eight_eleven_explicable = await db.morning_report(
        first_value=8, second_value=11, check_teacher='❎', current_date=current_date
    )
    one_eleven_present = await db.morning_report(
        first_value=1, second_value=11, check_teacher='✅', current_date=current_date
    )
    one_eleven_absent = await db.morning_report(
        first_value=1, second_value=11, check_teacher='☑️', current_date=current_date
    )
    one_eleven_explicable = await db.morning_report(
        first_value=1, second_value=11, check_teacher='❎', current_date=current_date
    )
    for level in all_levels:
        all_students = await db.count_everyday_attendance(current_date=current_date, level=level[0])
        present = await db.count_everyday_morning_check(current_date=current_date, level=level[0], check_teacher='✅')
        absent = await db.count_everyday_morning_check(current_date=current_date, level=level[0], check_teacher='☑️')
        explicable = await db.count_everyday_morning_check(current_date=current_date, level=level[0], check_teacher='❎')
        if level[0] == '6-V':
            print(five_seven_absent)

    print(all_students)
    print(present)
    print(absent + explicable)
    print(first_four_present)


@dp.message_handler(F.text == 'Haftalik davomat', state='*')
async def view_weekly_attendance(message: types.Message):
    pass


@dp.message_handler(F.text == 'Oylik davomat', state='*')
async def view_monthly_attendance(message: types.Message):
    pass
