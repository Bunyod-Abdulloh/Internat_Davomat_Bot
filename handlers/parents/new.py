@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    # Create an inline keyboard with multiselect options
    inline_keyboard = types.InlineKeyboardMarkup(row_width=2)
    options = ["Option 1", "Option 2", "Option 3", "Option 4"]

    for option in options:
        if button_states.get(option, False):
            button_text = f"{option} ✅"
        else:
            option
    inline_keyboard.add(types.InlineKeyboardButton(text=button_text, callback_data=option))

    await message.reply("Select options:", reply_markup=inline_keyboard)

@dp.callback_query_handler(lambda callback_query: True)
async def handle_callback_query(callback_query: types.CallbackQuery):
    selected_option = callback_query.data

    # Toggle the button state
    button_states[selected_option] = not button_states.get(selected_option, False)

    # Update the inline keyboard
    inline_keyboard = types.InlineKeyboardMarkup(row_width=2)
    options = ["Option 1", "Option 2", "Option 3", "Option 4"]

    for option in options:
        button_text = f"{option} ✅" if button_states.get(option, False) else option
        inline_keyboard.add(types.InlineKeyboardButton(text=button_text, callback_data=option))

    # Edit the original message to show the updated keyboard
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text="Select options:",
        reply_markup=inline_keyboard
    )
