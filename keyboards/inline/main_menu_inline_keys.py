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


async def main_menu_ikeys(uz: bool = False, ru: bool = False):
    key = InlineKeyboardMarkup(row_width=1)
    if uz:
        key.add(
            InlineKeyboardButton(
                text="👨‍👨‍👧 Ota - ona", callback_data="parent_uz"
            ),
            InlineKeyboardButton(
                text="🏫 Sinf rahbar", callback_data="curator_uz"
            ),
            InlineKeyboardButton(
                text="🧑‍🏫 Tarbiyachi", callback_data="educator_uz"
            )
        )
    elif ru:
        pass
    return key
