from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.educators_inline_keys import educators_class_btn
from loader import dp
from states.educators_states import EducatorsWorkTime, EducatorsQuestionnaire


# ewt_ = Educators Work Time (handlers/educators/work_time)
@dp.callback_query_handler(state=EducatorsWorkTime.main)
async def e_w_t_main(call: types.CallbackQuery, state: FSMContext):
    if call.data == "edu_back":
        await call.message.edit_text(
            text="O'zingizga biriktirilgan sinfni tanlang:", reply_markup=await educators_class_btn()
        )
        await EducatorsQuestionnaire.select_class.set()

    # elif call.data == "edu_morning":

