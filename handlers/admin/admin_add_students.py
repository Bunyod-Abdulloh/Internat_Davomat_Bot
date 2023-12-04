from aiogram import types

from loader import dp, db


@dp.message_handler(text='salom', state='*')
async def sampler(message: types.Message):
    await db.add_student(
        student="Aziza",
        class_number="6-V"
    )
    await message.answer(
        text="Qo'shildi!"
    )
