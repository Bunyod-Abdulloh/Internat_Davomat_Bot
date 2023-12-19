from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from states.teachers_state import TeachersAnketa


# ts_m_ = Teachers Main (handlers/teachers/file_name)
@dp.callback_query_handler(text="form_master", state="*")
async def ts_m_main(call: types.CallbackQuery):
    await call.message.edit_text(
        text="Ism-sharif va otaningizni ismini kiriting: "
             "\n\n<b>Namuna: Xaitova Barno Axmedovna</b>"
    )
    await TeachersAnketa.get_fullname.set()


@dp.message_handler(state=TeachersAnketa.get_fullname)
async def ts_m_get_fullname(message: types.Message, state: FSMContext):
    await state.update_data(
        teacher_fullname=message.text
    )
    await message.answer(
        text="Faningiz nomini tanlang:"
    )
    await TeachersAnketa.get_lesson.set()


@dp.callback_query_handler(state=TeachersAnketa.get_lesson)
async def ts_m_get_lesson(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(
        teacher_lesson=call.data
    )
    await call.message.edit_text(
        text="Ish kunlaringizni tanlang:"
    )
    await TeachersAnketa.get_work_days.set()


@dp.callback_query_handler(state=TeachersAnketa.get_work_days)
async def ts_m_get_work_days(call: types.CallbackQuery, state: FSMContext):
    print(call.data)
