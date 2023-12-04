from aiogram import types

from loader import dp, db


@dp.message_handler(text='salom', state='*')
async def sampler(message: types.Message):
    await db.add_student(
        student_number="1",
        student_fullname="Aziza Abdulloh qizi",
        class_number="6-V",
        telegram_id=message.from_user.id
    )
    await message.answer(
        text="Qo'shildi!"
    )
