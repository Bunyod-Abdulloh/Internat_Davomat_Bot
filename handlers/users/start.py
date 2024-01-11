from aiogram import types
from magic_filter import F

from loader import dp


@dp.message_handler(F.text == "salom", state="*")
async def samplera(message: types.Message):
    key = types.ReplyKeyboardMarkup(resize_keyboard=True)
    key.insert(types.KeyboardButton(
        text="Get url!", web_app=types.WebAppInfo(
            url="https://login.emaktab.uz/?ReturnUrl=https%3a%2f%2femaktab.uz%2f"
        )
    ))
    await message.answer(text=message.text, reply_markup=key)
