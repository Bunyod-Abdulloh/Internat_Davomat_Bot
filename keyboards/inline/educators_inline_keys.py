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


async def edu_work_time(class_number: str, morning: str, half_day: str, all_day: str, back: str):
    key = InlineKeyboardMarkup(row_width=1)
    key.add(
        InlineKeyboardButton(
            text=f"🌄 {morning}", callback_data=f"edumorning_{class_number}"
        ),
        InlineKeyboardButton(
            text=f"⏱ {half_day}", callback_data=f"eduhalf_{class_number}"
        ),
        InlineKeyboardButton(
            text=f"⏳ {all_day}", callback_data=f"eduallday_{class_number}"
        )
    )
    key.add(
        InlineKeyboardButton(
            text=f"⬅️ {back}", callback_data="edu_back"
        )
    )
    return key


async def educators_class_btn():
    classes = await db.get_educators_class()
    key = InlineKeyboardMarkup(row_width=4)
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
