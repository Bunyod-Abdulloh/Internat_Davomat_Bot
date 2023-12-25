from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db


async def view_students_uz(work_time: list, class_number: str, check: str, back: str, absent: str, present: str):
    key = InlineKeyboardMarkup(row_width=1)
    for student in work_time:
        key.add(
            InlineKeyboardButton(
                text=f"{student[1]}.{student[3]} {student[4]}",
                callback_data=f"stb_{student[0]}_{student[2]}"
            )
        )
    key.add(
        InlineKeyboardButton(
            text=absent, callback_data="absent_uz"
        )
    )
    key.add(
        InlineKeyboardButton(
            text=present, callback_data="present_uz"
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
