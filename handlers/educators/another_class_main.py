from aiogram import types

from loader import dp
from states.educators_states import EducatorsAnotherClass


@dp.callback_query_handler(state=EducatorsAnotherClass.main)
async def e_another_class(call: types.CallbackQuery):
    if call.data == "a":
        pass
