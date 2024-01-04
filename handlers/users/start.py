import os
import time
from datetime import datetime

import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import ADMINS
from keyboards.default.main_menu_cbuttons import main_menu_uz
from keyboards.inline.main_menu_inline_keys import select_language_ikeys
from loader import dp, bot


@dp.message_handler(text="salom", state="*")
async def samplera(message: types.Message):
    key = types.ReplyKeyboardMarkup(resize_keyboard=True)
    key.insert(types.KeyboardButton(
        text="Get url!", web_app=types.WebAppInfo(
            url="https://login.emaktab.uz/?ReturnUrl=https%3a%2f%2femaktab.uz%2f"
        )
    ))
    await message.answer(text=message.text, reply_markup=key)


@dp.message_handler(commands=['download'], state="*")
async def download_document(message: types.Message):
    # Replace 'YOUR_WEBSITE_URL' with the actual URL of the document you want to download
    website_url = 'https://schools.emaktab.uz/v2/excel?&action=gsb&group=2117942894751596410&filter=active'

    # Download the document from the website
    response = requests.get(website_url, stream=True)
    print(response)
    if response.status_code == 200:
        # Save the document with a desired name
        document_name = 'downloaded_document.xlsx'  # Change the name and extension as needed
        download_path = f'downloads/{document_name}'  # Save in 'downloads' folder

        with open(download_path, 'wb') as file:
            file.write(response.content)

        # Send the document to the user
        with open(download_path, 'rb') as file:
            await bot.send_document(message.chat.id, file)

        # Optional: Delete the downloaded file to save space
        os.remove(download_path)
    else:
        await message.answer(f"Failed to download document from {website_url}")


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message):
    print(message.from_user.full_name)

    await message.answer(
        text="Tilni tanlang:"
             "\n\nВыберите язык:",
        reply_markup=select_language_ikeys
    )


@dp.callback_query_handler(text="uz", state="*")
async def start_uz_main(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer(
        text="Tugmalardan birini tanlang:",
        reply_markup=main_menu_uz
    )



@dp.message_handler(text="🏡 Bosh sahifa", state="*")
async def main_menu_custom(message: types.Message, state: FSMContext):
    await message.answer(
        text="Kerakli bo'limni tanlang:", reply_markup=main_menu_uz
    )
    await state.finish()
