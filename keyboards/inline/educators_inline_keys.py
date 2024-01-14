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
        text="💰 Boshqa sinfda ishlash", callback_data=f"eik_another_uz"
    ),
    InlineKeyboardButton(
        text=f"⬅️ Ortga", callback_data="eik_back_uz"
    )
)


