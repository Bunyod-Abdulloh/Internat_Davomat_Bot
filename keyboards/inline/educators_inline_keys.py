from datetime import datetime

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
        text=f"⬅️ Ortga", callback_data="eik_back_uz"
    )
)


def check_work_button():
    buttons = InlineKeyboardMarkup(row_width=1)
    buttons.add(
        InlineKeyboardButton(
            text="👤 O'z sinfimda ishlayman!", callback_data="main_class_uz"
        ),
        InlineKeyboardButton(
            text="💰 Boshqa sinfda ishlash", callback_data=f"another_uz"
        )
    )
    return buttons


# ======== Section educators select_level ========
async def select_level_educators(telegram_id: int):
    user_classes = await db.select_check_work_telegram(telegram_id=telegram_id)
    key = InlineKeyboardMarkup(row_width=4)
    for level in user_classes:
        key.insert(
            InlineKeyboardButton(
                text=level[1], callback_data=level[1]
            )
        )
    key.add(
        InlineKeyboardButton(
            text="⬅️ Ortga", callback_data="back"
        )
    )
    return key


async def another_class_buttons(telegram_id: int, next_step: bool = None):
    all_classes = await db.select_all_classes()
    key = InlineKeyboardMarkup(row_width=4)
    for level in all_classes:
        attendance = await db.select_check_work(telegram_id=telegram_id, level=level[0])
        if attendance:
            button_text = f'✅ {level[0]}'
        else:
            button_text = f'☑️ {level[0]}'
        key.insert(
            InlineKeyboardButton(
                text=button_text, callback_data=level[0]
            )
        )
    key.add(
        InlineKeyboardButton(
            text="⬅️ Ortga", callback_data="back"
        )
    )
    if next_step:
        key.insert(
            InlineKeyboardButton(
                text="✅ Tasdiqlash", callback_data="check_another_uz"
            )
        )
    return key
