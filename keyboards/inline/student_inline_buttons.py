from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db


async def students_button(class_number: str):
    students = await db.get_students(
        class_number=class_number
    )
    print(students)
    key = InlineKeyboardMarkup(row_width=1)
    for student in students:
        key.add(
            InlineKeyboardButton(
                text=f"{student[1]}.{student[3]} | {student[-1]}",
                callback_data=f"stb_{student[0]}_{student[1]}"
            )
        )
    return key
