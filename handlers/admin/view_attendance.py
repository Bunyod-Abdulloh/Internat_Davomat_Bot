import os
from datetime import datetime

from aiogram import types
from magic_filter import F
from openpyxl.styles import Border, Side, Alignment

from data.config import ADMINS
from handlers.admin.a_functions import send_xlsx
from keyboards.default.admin_custom_buttons import admin_attendance_cbuttons
from openpyxl import Workbook
from loader import dp, db, bot


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
    for level in all_levels:
        level_ = f'{level[0]}-{level[1]}'
        check_level = await db.select_check_work_teacher(checked_date=current_date, level=level_)
        if check_level is None:
            count_no += 1
            not_submitted += f'{count_no}. {level_}\n'
        else:
            count_yes += 1
            submitted += f'{count_yes}. {level_}\n'
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

    wb = Workbook()
    ws = wb.active
    ws.append(['Sana:', new_date, '', '', '', ''])
    ws.append(['№', 'Sinf', 'Umumiy o\'quvchilar soni', 'Kelgan o\'quvchilar soni',
               'Kelmagan o\'quvchilar soni', 'Yotoqxonada qoladigan o\'quvchilar soni'])

    await send_xlsx(current_date=current_date, all_levels=all_levels, ws=ws)

    max_row = ws.max_row
    start_cell = ws['A2']
    end_cell = ws[f'F{max_row}']
    border_style = Border(left=Side(border_style='thin'),
                          right=Side(border_style='thin'),
                          top=Side(border_style='thin'),
                          bottom=Side(border_style='thin'))
    alignment_style = Alignment(horizontal='center', vertical='center', wrap_text=True)

    for row in ws.iter_rows(min_row=start_cell.row, max_row=end_cell.row,
                            min_col=start_cell.column, max_col=end_cell.column):
        for cell in row:
            cell.border = border_style
            cell.alignment = alignment_style
    wb.save("Kunlik_hisobot.xlsx")

    await bot.send_document(chat_id=ADMINS[0],
                            document=types.InputFile(path_or_bytesio="Kunlik_hisobot.xlsx")
                            )
    await message.answer(
        text=f'Joriy sana: {new_date}\nMa\'lumotlar to\'g\'riligini faylni yuklab olgach tekshirib '
             f'ko\'rishni unutmang!',
        reply_markup=await send_xlsx(current_date=current_date, all_levels=all_levels, button=True)
    )
    os.remove("Kunlik_hisobot.xlsx")


@dp.message_handler(F.text == 'Haftalik davomat', state='*')
async def view_weekly_attendance(message: types.Message):
    pass


@dp.message_handler(F.text == 'Oylik davomat', state='*')
async def view_monthly_attendance(message: types.Message):
    pass
