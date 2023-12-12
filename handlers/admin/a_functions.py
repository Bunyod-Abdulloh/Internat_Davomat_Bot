from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.admin_edit_educator_buttons import edit_educators
from keyboards.inline.main_menu_inline_keys import main_menu_keys
from loader import dp


# admin educators line 26
async def educator_main_first(educator_id: str, call: types.CallbackQuery, educator: list, employee: str,
                              first_phone: str, class_: str):
    await call.message.edit_text(
        text=f"{employee}: {educator[1]}"
             f"\n{first_phone}: {educator[2]}"
             f"\n{class_}: {educator[4]}",
        reply_markup=await edit_educators(
            telegram_id=educator_id
        )
    )


# admin educators line 31
async def educator_main_second(educator_id: str, call: types.CallbackQuery, educator: list, employee: str,
                               first_phone: str, second_phone: str, class_: str):
    await call.message.edit_text(
        text=f"{employee}: {educator[1]}"
             f"\n{first_phone}: {educator[2]}"
             f"\n{second_phone}: {educator[3]}"
             f"\n{class_}: {educator[4]}",
        reply_markup=await edit_educators(
            telegram_id=educator_id,
            second_phone=True
        )
    )
