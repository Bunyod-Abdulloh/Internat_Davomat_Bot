from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from keyboards.inline.student_inline_buttons import view_students_uz
from loader import dp, db


@dp.message_handler(F.text == 'salom', state='*')
async def sampler_handler(message: types.Message, state: FSMContext):
    await message.answer(
        text="O'quvchilarni kelgan kelmaganligini tugmalardan birini tanlab belgilang:",
        reply_markup=await view_students_uz(
            class_number="6-V"
        )
    )
    await state.update_data(
        count=0
    )
    await state.set_state("buttons")


@dp.callback_query_handler(state='buttons')
async def sampler_two(call: types.CallbackQuery, state: FSMContext):

    await call.answer(cache_time=0)
    data = await state.get_data()
    count = data['count']
    student_id = call.data.split("_")[1]
    get_student = await db.get_student_id(
        id_number=student_id
    )
    class_number = get_student[2]

    if call.data:
        count += 1
        if count == 1:
            if get_student[3] == "✅":
                await db.update_mark_student(
                    mark="❎",
                    id_number=student_id
                )
            else:
                await db.update_mark_student(
                    mark="✅",
                    id_number=student_id
                )

        elif count == 2:
            if get_student[3] == "❎":
                await db.update_mark_student(
                    mark="✅",
                    id_number=student_id
                )
            else:
                await db.update_mark_student(
                    mark="❎",
                    id_number=student_id
                )
            count = 0

        await state.update_data(
            count=count
        )
    absent = await db.count_mark(class_number=class_number, mark="✅")
    present = await db.count_mark(class_number=class_number, mark="❎")
    # await call.message.edit_text(
    #     text=f"Kelgan o'quvchilar soni: {absent}"
    #          f"\nKelmagan o'quvchilar soni: {present}",
    #     reply_markup=await view_students_uz(
    #         class_number=class_number
    #     )
    # )
