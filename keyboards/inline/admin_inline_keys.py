from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db


async def admin_check_button(user_id):

    key = InlineKeyboardMarkup(row_width=2)
    key.row(
        InlineKeyboardButton(
            text="❌ Bekor qilish",
            callback_data=f"admincancel_{user_id}"
        ),
        InlineKeyboardButton(
            text="✅ Tasdiqlash",
            callback_data=f"admincheck_{user_id}"
        )
    )
    return key


admin_check_keyboard = InlineKeyboardMarkup(row_width=2)
admin_check_keyboard.row(
    InlineKeyboardButton(
        text="❌ Bekor qilish",
        callback_data="canceladmin"
    ),
    InlineKeyboardButton(
        text="✅ Tasdiqlash",
        callback_data="checkadmin"
    )
)

admin_main_button = InlineKeyboardMarkup(row_width=1)
admin_main_button.add(
    InlineKeyboardButton(
        text="👨‍👨‍👧 Ota - onalar",
        callback_data="admin_parents_main"
    ),
    InlineKeyboardButton(
        text="🏫 Sinf rahbarlar",
        callback_data="adminteachers_main"
    ),
    InlineKeyboardButton(
        text="🧑‍🏫 Tarbiyachilar",
        callback_data="admin_educatorsmain"
    )
)


async def admin_view_educators_button():
    educators = await db.select_all_educators()
    key = InlineKeyboardMarkup(row_width=2)
    print(f"{educators} admin ikeys 54")
    for educator in educators:
        key.insert(
            InlineKeyboardButton(
                text=educator[1],
                callback_data=educator[0]
            )
        )
        key.add(
            InlineKeyboardButton(
                text="⬅️ Ortga",
                callback_data="adminmain_back"
            )
        )
    return key
