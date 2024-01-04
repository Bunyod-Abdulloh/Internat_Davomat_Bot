from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

select_language_ikeys = InlineKeyboardMarkup(row_width=1)
select_language_ikeys.row(
    InlineKeyboardButton(
        text="O'zbek", callback_data="uz"
    ),
    InlineKeyboardButton(
        text="Русский", callback_data="rus"
    )
)
