from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db


async def view_students_uz(work_time: list, class_number: str):
    key = InlineKeyboardMarkup(row_width=1)

    absent = await db.count_morning_check(class_number=class_number, morning_check="✅")
    present = await db.count_morning_check(class_number=class_number, morning_check="🔘")
    explicable = await db.count_morning_check(class_number=class_number, morning_check="🟡")

    for student in work_time:
        key.add(
            InlineKeyboardButton(
                text=f"{student[2]} {student[3]}",
                callback_data=f"stb_{student[0]}_{student[1]}"
            )
        )

    key.row(
        InlineKeyboardButton(
            text=f"✅ : {absent} ta", callback_data="absent_uz"
        ),
        InlineKeyboardButton(
            text=f"🔘 : {present}", callback_data="present_uz"
        ),
        InlineKeyboardButton(
            text=f"🟡 : {explicable}", callback_data="explicable_uz"
        )
    )
    key.row(
        InlineKeyboardButton(
            text=f"⬅️ Ortga",
            callback_data=f"stbback_{class_number}"
        ),
        InlineKeyboardButton(
            text=f"☑️ Tasdiqlash",
            callback_data=f"stbcheck_{class_number}"
        )
    )
    return key
