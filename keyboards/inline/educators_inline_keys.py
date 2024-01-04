from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db

# ======== Section add educators ========
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

# ======== Section educators main ========
educators_main_uz = InlineKeyboardMarkup(row_width=1)
educators_main_uz.add(
    InlineKeyboardButton(
        text="✅ Ishga keldim!", callback_data=f"eik_check_uz"
    ),
    InlineKeyboardButton(
        text="📊 Davomatni kiritish", callback_data=f"eik_attendance_uz"
    ),
    InlineKeyboardButton(
        text="👤 Shaxsiy kabinet", callback_data=f"eik_cabinet_uz"
    ),
    InlineKeyboardButton(
        text="💰 Boshqa sinfda ishlash", callback_data=f"eik_another_uz"
    ),
    InlineKeyboardButton(
        text=f"⬅️ Ortga", callback_data="eik_back_uz"
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
            text=f"⬅️ {back}", callback_data=f"eduback_{class_number}"
        )
    )
    return key


async def educators_class_btn():
    classes = await db.get_educators_class()
    key = InlineKeyboardMarkup(row_width=3)

    for class_ in classes:
        key.insert(
            InlineKeyboardButton(
                text=f"{class_[0]} {class_[1]}",
                callback_data=class_[0]
            )
        )
    key.row(
        InlineKeyboardButton(
            text="⬅️ Ortga",
            callback_data="eduback_one"
        ),
        InlineKeyboardButton(
            text="Davom etish ➡️",
            callback_data="educontinue"
        )
    )
    return key
