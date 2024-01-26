from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import db


async def generate_multiselect_keyboard(telegram_id: int, next_step: bool = False):
    key = InlineKeyboardMarkup(row_width=4)
    classes = await db.select_all_classes()
    for class_ in classes:
        level = f'{class_[0]}-{class_[1]}'
        user = await db.select_employee_level(telegram_id=telegram_id, level=level, position='Tarbiyachi')
        if user:
            button_text = f"✅ {level}"
        else:
            button_text = f"{level}"
        callback_data = f'multiselect_{level}'
        button = InlineKeyboardButton(text=button_text, callback_data=callback_data)
        key.insert(button)
    key.add(
        InlineKeyboardButton(
            text="⬅️ Ortga",
            callback_data="eduback_one"
        )
    )
    if next_step:
        key.insert(
            InlineKeyboardButton(
                text="Davom etish ➡️",
                callback_data="educontinue"
            )
        )
    return key


async def teachers_multiselect_keyboard(telegram_id: int, next_step: bool = False):
    key = InlineKeyboardMarkup(row_width=4)
    classes = await db.select_all_classes()
    for class_ in classes:
        level = f'{class_[0]}-{class_[1]}'
        user = await db.select_employee_level(telegram_id=telegram_id, level=level, position='Sinf rahbar')
        if user:
            button_text = f"✅ {level}"
        else:
            button_text = f"{level}"
        callback_data = f'multiselect_{level}'
        button = InlineKeyboardButton(text=button_text, callback_data=callback_data)
        key.insert(button)
    key.add(
        InlineKeyboardButton(
            text="⬅️ Ortga",
            callback_data="eduback_one"
        )
    )
    if next_step:
        key.insert(
            InlineKeyboardButton(
                text="Davom etish ➡️",
                callback_data="educontinue"
            )
        )
    return key


async def parents_main_ikb(telegram_id: int, next_step: bool = False):
    levels = await db.select_all_classes()
    key = InlineKeyboardMarkup(row_width=4)
    for n in levels:
        level = f'{n[0]}-{n[1]}'
        parents = await db.get_parents_level(parents_telegram=telegram_id, level=level)
        if parents:
            button_text = f'✅ {level}'
        else:
            button_text = level
        key.insert(InlineKeyboardButton(
            text=button_text, callback_data=f'plevel_{level}'
        ))
    key.add(
        InlineKeyboardButton(
            text="⬅️ Ortga",
            callback_data="parents_back"
        )
    )
    if next_step:
        key.insert(
            InlineKeyboardButton(
                text="Davom etish ➡️",
                callback_data="parents_next"
            )
        )
    return key
