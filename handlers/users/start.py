from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.start_keyboard import menu
from keyboards.inline.main_menu_inline_keys import select_language_ikeys, main_menu_ikeys
from loader import dp


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message):
    print(message.from_user.full_name)
    await message.answer(
        text="Assalomu alaykum! Internat_Botimizga xush kelibsiz!",
        reply_markup=menu
    )
    await message.answer(
        text="Tilni tanlang:"
             "\n\nВыберите язык:",
        reply_markup=select_language_ikeys
    )


@dp.callback_query_handler(text="uz", state="*")
async def start_uz_main(call: types.CallbackQuery):
    await call.message.edit_text(
        text="Tugmalardan birini tanlang:",
        reply_markup=await main_menu_ikeys(uz=True)
    )


@dp.message_handler(text="🏡 Bosh sahifa", state="*")
async def main_menu_custom(message: types.Message, state: FSMContext):

    await message.answer(
        text="Kerakli bo'limni tanlang:", reply_markup=await main_menu_ikeys(uz=True)
    )
    await state.finish()
