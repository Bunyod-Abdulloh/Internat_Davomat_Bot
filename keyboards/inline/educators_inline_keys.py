from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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

edu_work_time = InlineKeyboardMarkup(row_width=2)
edu_work_time.row(
    InlineKeyboardButton(
        text="🌄 Ertalabki", callback_data="edu_morning"
    ),
    InlineKeyboardButton(
        text="☀️ Kunduzgi", callback_data="edu_day"
    )
)
edu_work_time.add(
    InlineKeyboardButton(
        text="⬅️ Ortga", callback_data="edu_back"
    )
)
