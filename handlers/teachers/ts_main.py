from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from keyboards.inline.main_menu_inline_keys import select_language_ikeys
from keyboards.inline.teachers_inline_buttons import senior_lessons_ibutton, select_language_teachers
from loader import dp, db
from states.teachers_state import TeachersAnketa


# ts_m_ = Teachers Main (handlers/teachers/file_name)
@dp.callback_query_handler(F.data == "tr_main", state="*")
async def ts_m_main(call: types.CallbackQuery):
    await call.message.edit_text(
        text="Dars o'tish tilini tanlang:", reply_markup=select_language_teachers
    )


@dp.callback_query_handler(F.data == "uz_teach", state="*")
async def ts_m_get_fullname(call: types.CallbackQuery):
    await call.message.edit_text(
        text="Ism-sharif va otaningizni ismini kiriting: "
             "\n\n<b>Namuna: Xaitova Barno Axmedovna</b>"
    )
    await TeachersAnketa.get_fullname.set()


@dp.message_handler(state=TeachersAnketa.get_fullname)
async def ts_m_get_fullname(message: types.Message, state: FSMContext):

    await db.add_teacher(
        fullname=message.text, telegram_id=message.from_user.id
    )
    await state.update_data(
        teacher_counter=0
    )
    await message.answer(
        text="Faningiz nomini tanlang:", reply_markup=await senior_lessons_ibutton(
            back_step="Ortga", next_step="Keyingi", language_uz=True
        )
    )
    await TeachersAnketa.get_lesson.set()


@dp.callback_query_handler(state=TeachersAnketa.get_lesson)
async def ts_m_get_lesson(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=0)
    data = await state.get_data()
    counter = data['teacher_counter']
    lesson_name = call.data
    get_teacher = await db.get_teacher(
        telegram_id=call.from_user.id
    )

    counter += 1
    if counter == 1:
        if get_teacher[2] == "✅":
            await db.update_lesson_name(
                mark="🔘", lesson_name=lesson_name, telegram_id=call.from_user.id
            )
        else:
            await db.update_lesson_name(
                mark="✅", lesson_name=lesson_name, telegram_id=call.from_user.id
            )

    elif counter == 2:
        if get_teacher[2] == "🔘":
            await db.update_lesson_name(
                mark="✅", lesson_name=lesson_name, telegram_id=call.from_user.id
            )
        else:
            await db.update_lesson_name(
                mark="🔘", lesson_name=lesson_name, telegram_id=call.from_user.id
            )
        counter = 0

    await state.update_data(
        teacher_counter=counter
    )
    get_teacher = await db.get_teacher(
        telegram_id=call.from_user.id
    )
    print(get_teacher)
    await call.message.answer(
        text="Faningiz nomini tanlang:", reply_markup=await senior_lessons_ibutton(
            back_step="Ortga", next_step="Keyingi", language_uz=True
        )
    )

    # get_lesson = await db.
    # counter += 1
    #
    # if counter == 1:

    # await call.message.edit_text(
    #     text=f"Faningiz nomini tanlang:", reply_markup=await senior_lessons_ibutton(
    #         back_step="Ortga", next_step="Keyingi", language_uz=True
    #     )
    # )

    #
    # await state.update_data(
    #     teacher_lesson=call.data
    # )
    # await call.message.edit_text(
    #     text="Ish kunlaringizni tanlang:"
    # )
    # await TeachersAnketa.get_work_days.set()


@dp.callback_query_handler(state=TeachersAnketa.get_work_days)
async def ts_m_get_work_days(call: types.CallbackQuery, state: FSMContext):
    print(call.data)
