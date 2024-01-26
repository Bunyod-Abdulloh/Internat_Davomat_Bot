import os
from datetime import datetime

from aiogram import types
from magic_filter import F

from handlers.admin.a_functions import send_xlsx
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
    date = f'Sana: {current_date}\n\n'
    submitted = 'Davomat topshirgan sinflar:\n'
    not_submitted = '\nDavomat topshirmagan sinflar:\n'
    count_yes = 0
    count_no = 0
    for n in all_levels:
        level = f'{n[0]}-{n[1]}'
        check_level = await db.select_check_work_teacher(checked_date=current_date, level=level)
        if check_level is None:
            count_no += 1
            not_submitted += f'{count_no}. {level}\n'
        else:
            count_yes += 1
            submitted += f'{count_yes}. {level}\n'
    await message.answer(
        text=date + submitted + not_submitted
    )


@dp.message_handler(F.text == 'Kunlik davomat', state='*')
async def view_everydays_attendance(message: types.Message):
    current_date = datetime.now().date()
    source_format = "%Y-%m-%d"
    data = datetime.strptime(str(current_date), source_format)
    new_date = data.strftime("%d.%m.%Y")
    all_levels = await db.all_levels_attendance(current_date=current_date)
    text = await send_xlsx(current_date=current_date, all_levels=all_levels, new_date=new_date)
    await message.answer_document(
        document=types.InputFile(path_or_bytesio="Kunlik_hisobot.xlsx"),
        caption=text
    )
    os.remove("Kunlik_hisobot.xlsx")


@dp.message_handler(F.text == 'Haftalik davomat', state='*')
async def view_weekly_attendance(message: types.Message):
    await message.answer(
        text='Ushbu bo\'lim hozircha ishlamaydi!'
    )


@dp.message_handler(F.text == 'Oylik davomat', state='*')
async def view_monthly_attendance(message: types.Message):
    await message.answer(
        text='Ushbu bo\'lim hozircha ishlamaydi!'
    )
