from aiogram import types
from magic_filter import F

from keyboards.default.main_menu_cbuttons import main_menu_uz
from keyboards.inline.all_inline_keys import parents_main_ikb
from loader import dp, db


@dp.message_handler(F.text == '👨‍👨‍👧 Ota - ona', state='*')
async def parents_main_cmd(message: types.Message):
    await message.answer(
        text='Kerakli sinf yoki sinflarni tanlang:',
        reply_markup=await parents_main_ikb(
            telegram_id=message.from_user.id
        )
    )


@dp.callback_query_handler(F.data.contains('plevel_'), state='*')
async def parents_select_level(call: types.CallbackQuery):
    level = call.data.split('_')[1]
    parents_telegram = call.from_user.id
    parents = await db.get_parents_level(
        parents_telegram=parents_telegram, level=level
    )
    if parents:
        await db.delete_parents(
            parents_telegram=parents_telegram, level=level
        )
    else:
        await db.add_parents(
            parents_telegram=parents_telegram, level=level
        )
    await call.message.edit_text(
        text='Kerakli sinf yoki sinflarni tanlang:',
        reply_markup=await parents_main_ikb(
            telegram_id=parents_telegram, next_step=True
        )
    )


@dp.callback_query_handler(F.data == 'parents_back', state='*')
async def back_parents(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer(
        text='Bosh sahifa', reply_markup=main_menu_uz
    )


@dp.callback_query_handler(F.data == 'parents_next', state='*')
async def next_step_parents(call: types.CallbackQuery):
    await call.message.delete()
    parents_telegram = call.from_user.id
    parents = await db.get_parents(parents_telegram=parents_telegram)
    for n in parents:
        level = n[0]
        employee = await db.get_educator_checker(level=level, check_work=True)
        if employee:
            educator = await db.select_employee_level(telegram_id=employee[0], level=level, position='Tarbiyachi')
            if educator[3] is None:
                await call.message.answer(
                    text=f'<b>Bugun ishda:</b>'
                         f'\n\nTarbiyachi: {educator[1]}'
                         f'\n\nTelefon raqam: {educator[2]}'
                         f'\n\nSinf: {educator[0]}'
                )
            else:
                await call.message.answer(
                    text=f'<b>Bugun ishda:</b>'
                         f'\n\nTarbiyachi: {educator[1]}'
                         f'\n\nTelefon raqam: {educator[2]}'
                         f'\n\nIkkinchi telefon raqam: {educator[3]}'
                         f'\n\nSinf: {educator[0]}'
                )
        else:
            await call.message.answer(
                text=f'{level} sinf tarbiyachisi ma\'lumotlari topilmadi!'
            )
    await db.delete_parents_(parents_telegram=parents_telegram)
