from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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
