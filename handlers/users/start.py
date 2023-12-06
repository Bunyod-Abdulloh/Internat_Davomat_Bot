from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.inline.main_menu_inline_keys import main_menu_keys
from loader import dp, db


async def students_button(class_number: str):
    students = await db.get_students(
        class_number=class_number
    )
    key = types.InlineKeyboardMarkup(row_width=1)
    for student in students:
        key.add(
            types.InlineKeyboardButton(
                text=f"{student[2]} {student[-1]}",
                callback_data=f"stb_{student[0]}_{student[1]}"
            )
        )
    return key


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message):
    await message.answer(
        text="Assalomu alaykum! Internat_Botimizga xush kelibsiz!"
             "\n\nTugmalardan birini tanlang:",
        reply_markup=main_menu_keys
    )


@dp.message_handler(text='salom', state='*')
async def sampler_handler(message: types.Message, state: FSMContext):
    await message.answer(
        text="O'quvchilarni kelgan kelmaganligini tugmalardan birini tanlab belgilang:",
        reply_markup=await students_button(
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
    class_number = call.data.split("_")[-1]
    get_student = await db.get_student_id(
        id_number=student_id
    )

    if call.data:
        count += 1
        if count == 1:
            if get_student[3] == "✅":
                await db.update_mark_student(
                    mark="❌",
                    id_number=student_id
                )
            else:
                await db.update_mark_student(
                    mark="✅",
                    id_number=student_id
                )

        elif count == 2:
            if get_student[3] == "❌":
                await db.update_mark_student(
                    mark="✅",
                    id_number=student_id
                )
            else:
                await db.update_mark_student(
                    mark="❌",
                    id_number=student_id
                )
            count = 0

        await state.update_data(
            count=count
        )
    # present = await db.count_mark(class_number=class_number, mark="✅")
    # absent = await db.count_mark(class_number=class_number, mark="❌")
    await call.message.edit_text(
        text=f"Kelgan o'quvchilar soni: "
             f"\nKelmagan o'quvchilar soni:",
        reply_markup=await students_button(
            class_number=class_number
        )
    )
# {present} {absent}