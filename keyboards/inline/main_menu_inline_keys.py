from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_menu_keys = InlineKeyboardMarkup(row_width=2)
main_menu_keys.row(
    InlineKeyboardButton(
        text="Ota - ona",
        callback_data="parent"
    ),
    InlineKeyboardButton(
        text="Sinf rahbar",
        callback_data="form_master"
    )
)
main_menu_keys.add(
    InlineKeyboardButton(
        text="Tarbiyachi",
        callback_data="educator"
    )
)
