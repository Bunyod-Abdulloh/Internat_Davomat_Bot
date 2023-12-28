from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db


async def view_students_uz(work_time: list, class_number: str, check: str, back: str, absent: str, present: str,
                           uz: bool = False, ru: bool = False):
    key = InlineKeyboardMarkup(row_width=1)

    for student in work_time:
        key.add(
            InlineKeyboardButton(
                text=f"{student[2]} {student[3]}",
                callback_data=f"stb_{student[0]}_{student[1]}"
            )
        )
    if uz:
        key.row(
            InlineKeyboardButton(
                text=f"{present}", callback_data="present_uz"
            ),
            InlineKeyboardButton(
                text=f"{absent}", callback_data="absent_uz"
            )
        )
    elif ru:
        key.add(
            InlineKeyboardButton(
                text=f"{absent} | {present}", callback_data="absent_ru"
            )
        )
    key.row(
        InlineKeyboardButton(
            text=f"⬅️ {back}",
            callback_data=f"stbback_{class_number}"
        ),
        InlineKeyboardButton(
            text=f"☑️ {check}",
            callback_data=f"stbcheck_{class_number}"
        )
    )
    return key
