from aiogram.types import ReplyKeyboardMarkup

admin_custom_btn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
admin_custom_btn.row("Davomat")
admin_custom_btn.row("O'quvchilarni qo'shish (excel shaklda)")
admin_custom_btn.row("↩️ Bosh sahifaga qaytish")

admin_attendance_cbuttons = ReplyKeyboardMarkup(resize_keyboard=True)
admin_attendance_cbuttons.row('Sinflar davomati')
admin_attendance_cbuttons.row('Kunlik davomat', 'Haftalik davomat')
admin_attendance_cbuttons.row('Oylik davomat')
admin_attendance_cbuttons.row("🔙 Ortga")
