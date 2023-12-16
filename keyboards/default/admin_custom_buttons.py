from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_custom_btn = ReplyKeyboardMarkup(resize_keyboard=True)
admin_custom_btn.row("Ota-onalar", "Sinf rahbarlar")
admin_custom_btn.row("Tarbiyachilar", "O'quvchilar")
admin_custom_btn.row("🏡 Bosh sahifa")

admin_custom_students = ReplyKeyboardMarkup(resize_keyboard=True)
admin_custom_students.row("Sinf qo'shish", "Sinf o'chirish")
admin_custom_students.row("O'quvchi qo'shish", "O'quvchi o'chirish")
admin_custom_students.row("O'quvchilarni qo'shish (excel shaklda)")
admin_custom_students.row("🔙 Ortga")
