from aiogram import types

from loader import dp
from states.educators_states import EducatorsAnotherClass


@dp.callback_query_handler(state=EducatorsAnotherClass.main)
async def e_another_class(call: types.CallbackQuery):
    telegram_id = call.from_user.id
    if call.data.__contains__("multiselect_"):
        class_number = call.data.split('_')[1]
        print(class_number)
