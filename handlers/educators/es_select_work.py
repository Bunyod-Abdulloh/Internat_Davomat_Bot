from datetime import datetime

from aiogram import types

from keyboards.default.educator_buttons import educators_main_buttons
from loader import dp, db
from states.educators_states import EducatorsSelectWork


@dp.callback_query_handler(state=EducatorsSelectWork.main)
async def select_work_main(call: types.CallbackQuery):

    telegram_id = call.from_user.id
    classes = await db.select_employee_return_list(telegram_id=telegram_id)
    attendance = await db.get_educator_morning(educator_id=classes[0][1])



