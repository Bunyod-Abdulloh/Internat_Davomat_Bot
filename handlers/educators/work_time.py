from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from states.educators_states import EducatorsWorkTime


# ewt_ = Educators Work Time (handlers/educators/work_time)
@dp.callback_query_handler(state=EducatorsWorkTime.main)
async def e_w_t_main(call: types.CallbackQuery, state: FSMContext):
    if call.data == "":
        pass
    elif call.data == "":
        pass
