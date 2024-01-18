from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def educators_main_buttons():
    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons.add('✅ Ishga keldim!')
    buttons.row('👤 Shaxsiy kabinet', '📊 Davomat kiritish')
    buttons.row('🏡 Bosh sahifa')
    return buttons
