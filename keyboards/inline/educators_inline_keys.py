from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db

edu_phone_number = InlineKeyboardMarkup(row_width=2)
edu_phone_number.row(
    InlineKeyboardButton(
        text="Raqam kiritish",
        callback_data="add_edusecond_number"
    ),
    InlineKeyboardButton(
        text="Raqamim bitta",
        callback_data="edu_number_first"
    )
)

edu_work_time = InlineKeyboardMarkup(row_width=1)
edu_work_time.row(
    InlineKeyboardButton(
        text="🌄 Ertalabki", callback_data="edu_morning"
    ),
    InlineKeyboardButton(
        text="️⏳ Yarim kun", callback_data="edu_day"
    ),
    InlineKeyboardButton(
        text="⌛️ Bir kun", callback_data="edu_day"
    )
)
edu_work_time.add(
    InlineKeyboardButton(
        text="⬅️ Ortga", callback_data="edu_back"
    )
)


async def educators_class_btn():
    classes = await db.get_educators_class()
    key = InlineKeyboardMarkup(row_width=5)
    for class_ in classes:
        key.insert(
            InlineKeyboardButton(
                text=class_[0],
                callback_data=class_[0]
            )
        )
    key.add(
        InlineKeyboardButton(
            text="⬅️ Ortga",
            callback_data="eduback_one"
        )
    )
    return key
