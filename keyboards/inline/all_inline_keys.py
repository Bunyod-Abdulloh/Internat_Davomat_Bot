from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db


async def generate_multiselect_keyboard(telegram_id: int, table_from_db: list, next_step=False):
    key = InlineKeyboardMarkup(row_width=4)
    for class_ in table_from_db:
        user = await db.select_employee(telegram_id=telegram_id, level=class_[0])
        if user:
            button_text = f"✅ {class_[0]}"
        else:
            button_text = f"{class_[0]}"
        callback_data = f'multiselect_{class_[0]}'
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
