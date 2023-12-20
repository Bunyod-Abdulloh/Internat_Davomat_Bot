from aiogram import types

from keyboards.inline.teachers_inline_buttons import senior_classes_uz
from loader import dp, db
from states.admin_state import AdminTeachers


@dp.message_handler(state=AdminTeachers.main)
async def a_t_m_main(message: types.Message):
    if message.text == "O'qituvchi qo'shish":
        pass
    elif message.text == "O'qituvchi o'chirish":
        pass
    elif message.text == "Fanlarni ma'lumotlar bazasiga qo'shish":
        for lesson in senior_classes_uz:
            await db.add_lessons(
                lesson_name=lesson
            )
        await message.answer(
            text="Fanlar ma'lumotlar bazasiga qo'shildi!"
        )

    elif message.text == "Fanlarni ma'lumotlar bazasidan o'chirish":
        pass
    elif message.text == "Fan qo'shish":
        pass
    elif message.text == "Fan o'chirish":
        pass
    elif message.text == "🔙 Ortga":
        pass
