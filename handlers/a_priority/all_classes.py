# from aiogram import Bot, Dispatcher, types
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.types import CallbackQuery
#
# API_TOKEN = '6402238640:AAFTP_9xivBftWwF3dMd2OKMwUJr32yE2sI'
# bot = Bot(token=API_TOKEN)
# dp = Dispatcher(bot)
#
# # List of options for multiselect
# multiselect_options = ["Option 1"]
#
# user_selected_options = {}
#
#
# @dp.message_handler(commands=['start'])
# async def start_command(message: types.Message):
#     keyboard = generate_multiselect_keyboard()
#     await message.answer("Select multiple options:", reply_markup=keyboard)
#
#
# def generate_multiselect_keyboard():
#     keyboard = InlineKeyboardMarkup(row_width=2)
#     for option in multiselect_options:
#         selected = user_selected_options.get(option, False)
#         print(f"{selected} 25")
#         if selected:
#             button_text = f"✅ {option}"
#         else:
#             button_text = f"☑ {option}"
#         callback_data = f'multiselect_{option}'
#         button = InlineKeyboardButton(text=button_text, callback_data=callback_data)
#         keyboard.insert(button)
#     return keyboard
#
#
# @dp.callback_query_handler(lambda c: c.data.startswith('multiselect_'))
# async def process_multiselect_callback(callback_query: CallbackQuery):
#
#     option = callback_query.data.split('_')[1]
#     selected = user_selected_options.get(option, False)
#
#     print(f"{selected} 42")
#     user_selected_options[option] = not selected
#     print(f"{user_selected_options} 44")
#     print(f"{user_selected_options[option]} 43")
#
#     # Update the keyboard with the new selection state
#     await bot.edit_message_text(chat_id=callback_query.message.chat.id,
#                                 message_id=callback_query.message.message_id,
#                                 text="Select multiple options:",
#                                 reply_markup=generate_multiselect_keyboard())
#
#
# if __name__ == '__main__':
#     from aiogram import executor
#     executor.start_polling(dp, skip_updates=True)
