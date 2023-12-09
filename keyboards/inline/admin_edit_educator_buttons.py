from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# aeeb = Admin edit educator buttons (keyboards/inline/file-name)
async def edit_educators(telegram_id, second_phone=False):
    key = InlineKeyboardMarkup(row_width=1)
    key.add(
        InlineKeyboardButton(
            text="Ism - familiya o'zgartirish",
            callback_data=f"aeebname_{telegram_id}"
        ),
        InlineKeyboardButton(
            text="Telefon raqam o'zgartirish",
            callback_data=f"aeebfirstphone_{telegram_id}"
        )
    )
    if second_phone:
        key.add(InlineKeyboardButton(
            text="Ikkinchi raqam o'zgartirish",
            callback_data=f"aeebsecondphone_{telegram_id}"
        )
        )
    else:
        key.add(InlineKeyboardButton(
            text="Sinfni o'zgartirish",
            callback_data=f"aeebclass_{telegram_id}"
        ),
            InlineKeyboardButton(
                text="⬅️ Ortga",
                callback_data="aeeb_educatorslist"
            )
        )
    return key
