from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.admin_inline_keys import key_returner
from keyboards.inline.educators_inline_keys import educators_class_btn
from keyboards.inline.student_inline_buttons import students_button
from loader import dp, db
from states.educators_states import EducatorsWorkTime, EducatorsQuestionnaire


# e_w_t_ = Educators Work Time (handlers/educators/work_time)
@dp.callback_query_handler(state=EducatorsWorkTime.main)
async def e_w_t_main(call: types.CallbackQuery, state: FSMContext):
    if call.data == "edu_back":
        await call.message.edit_text(
            text="O'zingizga biriktirilgan sinfni tanlang:", reply_markup=await educators_class_btn()
        )
        await EducatorsQuestionnaire.select_class.set()

    elif call.data.__contains__("edumorning_"):
        class_number = call.data.split("_")[-1]
        students = await db.get_students(
            class_number=class_number
        )

        await call.message.edit_text(
            text="O'quvchilarni kelgan kelmaganligini tugmalarni bosib belgilang, yakunda <b>Tasdiqlash</b> tugmasini "
                 "bosing:",
            reply_markup=await students_button(class_number=class_number, back="Ortga", check="Tasdiqlash"
                                               )
        )
        await state.update_data(
            count=0
        )
        await state.set_state("buttons")

    elif call.data.__contains__("eduhalf_"):
        class_number = call.data.split("_")[-1]

    elif call.data.__contains__("eduday_"):
        class_number = call.data.split("_")[-1]
