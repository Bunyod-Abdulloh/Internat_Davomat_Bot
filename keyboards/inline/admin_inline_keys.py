from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_check_button(user_id):
    key = InlineKeyboardMarkup(row_width=2)
    key.row(
        InlineKeyboardButton(
            text="Bekor qilish",
            callback_data=f"admincancel_{user_id}"
        ),
        InlineKeyboardButton(
            text="Tasdiqlash",
            callback_data=f"admincheck_{user_id}"
        )
    )
    return key
