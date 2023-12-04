from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db


# aik = Admin inline keys (keyboards/inline/file_name)
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
        callback_data="aik_parents_main"
    ),
    InlineKeyboardButton(
        text="🏫 Sinf rahbarlar",
        callback_data="aikteachers_main"
    ),
    InlineKeyboardButton(
        text="🧑‍🏫 Tarbiyachilar",
        callback_data="aik_educatorsmain"
    )
)


async def admin_view_educators_button():
    educators = await db.select_all_educators()
    key = InlineKeyboardMarkup(row_width=2)
    for educator in educators:
        key.insert(
            InlineKeyboardButton(
                text=educator[1],
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


async def edit_educators(id_number):
    key = InlineKeyboardMarkup(row_width=1)
    key.add(
        InlineKeyboardButton(
            text="Ism - familiya o'zgartirish",
            callback_data=f"aikeditnameeducator_{id_number}"
        ),
        InlineKeyboardButton(
            text="Lavozim o'zgartirish",
            callback_data=f"aikeditposteducator_{id_number}"
        ),
        InlineKeyboardButton(
            text="Telefon raqam o'zgartirish",
            callback_data=f"aikeditphoneeducator_{id_number}"
        ),
        InlineKeyboardButton(
            text="Sinfini o'zgartirish",
            callback_data=f"aikeditclasseducator_{id_number}"
        ),
        InlineKeyboardButton(
            text="⬅️ Ortga",
            callback_data="aikback_educatorslist"
        )
    )
    return key
