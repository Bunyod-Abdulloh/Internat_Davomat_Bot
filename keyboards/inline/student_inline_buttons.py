from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db


async def view_students_uz(work_time: list, class_number: str, morning: bool = False, night: bool = False):
    key = InlineKeyboardMarkup(row_width=1)
    print(work_time)
    for student in work_time:
        key.add(
            InlineKeyboardButton(
                text=f"{student[1]} {student[2]}",
                callback_data=f"stb_{student[0]}_{class_number}"
            )
        )
    if morning:
        absent = await db.count_morning_check(class_number=class_number, morning_check="✅")
        present = await db.count_morning_check(class_number=class_number, morning_check="🔘")
        explicable = await db.count_morning_check(class_number=class_number, morning_check="🟡")

        key.row(
            InlineKeyboardButton(
                text=f"✅ : {absent} ta", callback_data=f"absentuz_{absent}"
            ),
            InlineKeyboardButton(
                text=f"🔘 : {present}", callback_data=f"presentuz_{present}"
            ),
            InlineKeyboardButton(
                text=f"🟡 : {explicable}", callback_data=f"explicableuz_{explicable}"
            )
        )
    elif night:
        absent = await db.count_night_check(class_number=class_number, night_check="✅")
        present = await db.count_night_check(class_number=class_number, night_check="🔘")

        key.row(
            InlineKeyboardButton(
                text=f"✅ : {absent} ta", callback_data=f"absentuz_{absent}"
            ),
            InlineKeyboardButton(
                text=f"🔘 : {present}", callback_data=f"presentuz_{present}"
            )
        )
    key.row(
        InlineKeyboardButton(
            text=f"⬅️ Ortga",
            callback_data=f"stbback"
        ),
        InlineKeyboardButton(
            text=f"☑️ Tasdiqlash",
            callback_data=f"stbcheck_{class_number}"
        )
    )
    return key
