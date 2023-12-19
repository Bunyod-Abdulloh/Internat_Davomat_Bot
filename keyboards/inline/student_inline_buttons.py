from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db


async def students_button(class_number: str, check: str, back: str, absent: str, present: str):
    students = await db.get_students(
        class_number=class_number
    )

    key = InlineKeyboardMarkup(row_width=1)
    for student in students:
        key.add(
            InlineKeyboardButton(
                text=f"{student[1]}.{student[3]} | {student[-1]}",
                callback_data=f"stb_{student[0]}_{class_number}"
            )
        )
    key.add(
        InlineKeyboardButton(
            text=absent, callback_data="absent"
        )
    )
    key.add(
        InlineKeyboardButton(
            text=present, callback_data="present"
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
