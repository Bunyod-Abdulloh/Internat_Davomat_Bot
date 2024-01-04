from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db


# aik = Admin inline keys (keyboards/inline/file_name)
async def admin_check_btn(user_id: int):
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
        callback_data="aik_parents_main"
    ),
    InlineKeyboardButton(
        text="🏫 Sinf rahbarlar",
        callback_data="aikteachers_main"
    ),
    InlineKeyboardButton(
        text="🧑‍🏫 Tarbiyachilar",
        callback_data="aik_educatorsmain"
    ),
    InlineKeyboardButton(
        text="🎓 O'quvchilar",
        callback_data="aik_students_main"
    )
)


async def admin_view_educators_btn():
    educators = await db.select_all_educators()
    key = InlineKeyboardMarkup(row_width=2)

    for educator in educators:
        key.insert(
            InlineKeyboardButton(
                text=f"{educator[4]} | {educator[1]} ",
                callback_data=f"aikeducatorid_{educator[0]}"
            )
        )
    key.add(
        InlineKeyboardButton(
            text="⬅️ Ortga",
            callback_data="aikback_adminpage"
        )
    )
    return key


def chunks(lst, n):
    empty_list = []
    for e in lst:
        empty_list.append(e)
    for i in range(0, len(lst), n):
        yield empty_list[i:i + n]


async def key_returner(items, current_page, all_pages):
    keys = InlineKeyboardMarkup(
        row_width=1
    )

    for i in items:
        keys.insert(
            InlineKeyboardButton(
                text=f"{i[2]} | {i[4]}",
                callback_data=f"{i[0]}"
            )
        )
    keys.row(
        InlineKeyboardButton(
            text="⬅️ Ortga",
            callback_data="-1"
        ),
        InlineKeyboardButton(
            text=f"{current_page}/{all_pages}",
            callback_data=f"alertmessage_{current_page}"
        ),
        InlineKeyboardButton(
            text="Oldinga ➡️",
            callback_data="+1"
        )
    )
    keys.add(
        InlineKeyboardButton(
            text="🏡 Bosh sahifa",
            callback_data="main_menu"
        )
    )
    return keys
