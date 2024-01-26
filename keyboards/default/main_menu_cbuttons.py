from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu_uz = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,
                                   input_field_placeholder='Kerakli bo\'limni tanlang')
main_menu_uz.row("👨‍👨‍👧 Ota - ona", "🏫 Sinf rahbar")
main_menu_uz.row("🧑‍🏫 Tarbiyachi")
