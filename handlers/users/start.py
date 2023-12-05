from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.inline.main_menu_inline_keys import main_menu_keys
from loader import dp


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message):

    await message.answer(
        text="Assalomu alaykum! Internat_Botimizga xush kelibsiz!"
             "\n\nTugmalardan birini tanlang:",
        reply_markup=main_menu_keys
    )


@dp.message_handler(text='salom', state='*')
async def sampler_handler(message: types.Message):
    key = types.InlineKeyboardMarkup(row_width=3)
    key.add(
        types.InlineKeyboardButton(
            text="Abdulxayev Muhammadzohir",
            callback_data="6-V",
        )
    )
    key.row(
        types.InlineKeyboardButton(
            text="✅",
            callback_data="check"
        ),
        types.InlineKeyboardButton(
            text="❌",
            callback_data="not"
        )
    )
    key.add(
        types.InlineKeyboardButton(
            text="Abdulxayev Firdavs",
            callback_data="firdavs"
        )
    )
    key.row(
        types.InlineKeyboardButton(
            text="✅",
            callback_data="check"
        ),
        types.InlineKeyboardButton(
            text="❌",
            callback_data="not"
        )
    )
    await message.answer(
        text="O'quvchilarni kelgan kelmaganligini tugmalardan birini tanlab belgilang:",
        reply_markup=key
    )
