from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db


async def generate_multiselect_keyboard(telegram_id: int = None, another: bool = False, next_step: bool = False):
    key = InlineKeyboardMarkup(row_width=4)
    classes = await db.select_all_classes()
    educator_id = await db.select_employee(telegram_id=telegram_id)
    print(educator_id)
    for class_ in classes:
        if another:
            user = await db.get_employee_attendance(educator_id=educator_id[2], level=class_[0])
        else:
            user = await db.select_employee_level(telegram_id=telegram_id, level=class_[0])
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
