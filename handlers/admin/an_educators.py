from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from handlers.admin.a_functions import educator_main_first, educator_main_second
from keyboards.inline.admin_inline_keys import admin_view_educators_btn, admin_main_button
from loader import dp, db
from states.admin_state import AdminEditEdicators


#  a_e = Admin educator (handlers/admin/file_name)
# @dp.callback_query_handler(F.data == 'aik_educatorsmain', state='*')
# async def a_e_main(call: types.CallbackQuery):
#     await call.message.edit_text(
#         text="Tarbiyachilar bo'limi",
#         reply_markup=await admin_view_educators_btn()
#     )

@dp.message_handler(F.text == "userlar", state="*")
async def a_e_userlar(message: types.Message):
    for sinf in classes_list:
        await db.add_educators_class(
            level=sinf
        )
    await message.answer(
        text="Sinflar qo'shildi!"
    )


@dp.callback_query_handler(F.text.contains('aikeducatorid_'), state='*')
async def a_e_get_educator_id(call: types.CallbackQuery):
    educator_id = call.data.split('_')[-1]
    educator = await db.select_by_id(
        id_number=educator_id
    )
    if educator[3] is None:
        await educator_main_first(
            educator_id=educator_id, call=call, educator=educator, employee="Hodim", first_phone="Telefon raqam",
            class_="Biriktirilgan sinf"
        )
    else:
        await educator_main_second(
            educator_id=educator_id, call=call, educator=educator, employee="Hodim", first_phone="Telefon raqam",
            second_phone="Ikkinchi telefon raqam", class_="Biriktirilgan sinf"
        )
    await AdminEditEdicators.main.set()


@dp.callback_query_handler(F.data == "aikback_adminpage", state="*")
async def a_e_back_adminpage(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        text="Admin bosh menyusi",
        reply_markup=admin_main_button
    )
    await state.finish()


@dp.callback_query_handler(F.data == "aeeb_educatorslist", state="*")
async def a_e_educatorslist(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        text="Tarbiyachilar bo'limi",
        reply_markup=await admin_view_educators_btn()
    )
    await state.finish()


CHANNEL_ID = -1001562489298
ITEMS = list(range(1, 40))


@dp.callback_query_handler(F.text.contains('alertmessage_'), state="*")
async def alert_message(call: types.CallbackQuery):
    current_page = call.data.split("_")[1]

    await call.answer(
        text=f"Siz {current_page} - sahifadasiz!", show_alert=True
    )


@dp.callback_query_handler(F.data == "aik_educatorsmain", state="*")
async def a_e_classes(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        text="Tarbiyachilar bo'limi\n\nKerakli sinfni tanlang:",
        reply_markup=await educators_class_btn_uz()
    )
    # c = 0
    # educators = await db.select_all_educators()
    # # print(f"{educators} 73")
    # datas = list(chunks(educators, 15))
    #
    # keys = await key_returner(
    #     items=datas[c], current_page=1, all_pages=len(datas)
    # )
    #
    # await call.message.answer(
    #     text="Tarbiyachilar bo'limi", reply_markup=keys
    # )
    # counter = c + 1
    # await state.update_data(
    #     c=c,
    #     len_datas=len(datas),
    #     counter=counter
    # )
    # await MuqriyVideoStates.qadamjolar_menu.set()

# @dp.callback_query_handler(state=MuqriyVideoStates.qadamjolar_menu)
# async def callback_resp(call: types.CallbackQuery, state: FSMContext):
#     await call.message.delete()
#
#     if call.data in LATEST_RESULT.keys():
#         await bot.copy_message(
#             chat_id=call.from_user.id,
#             from_chat_id=CHANNEL_ID,
#             message_id=LATEST_RESULT[call.data],
#             reply_markup=qadamjolar_back_button
#         )
#         await MuqriyVideoStates.qadamjolar_videos.set()
#
#     else:
#         data = await state.get_data()
#         c = data['c']
#         counter = data['counter']
#         len_datas = data['len_datas']
#
#         if call.data == "+1":
#             c = int(c) + 1
#             counter += 1
#         elif call.data == "-1":
#             c = int(c) - 1
#             counter -= 1
#         if c == len_datas or c == - len_datas:
#             c = 0
#             if c == 0 or c == 4:
#                 counter = 1
#
#         datas = list(chunks(ITEMS, 15))[c]
#
#         keys = await key_returner(
#             items=datas,
#             current_page=counter,
#             all_pages=len_datas
#         )
#
#         text = str()
#         for i in datas:
#             text += f"{MENU_POST[i - 1]}"
#         await call.message.answer(
#             text=text,
#             reply_markup=keys
#         )
#         await state.update_data(
#             c=c,
#             counter=counter
#         )
#
#
# @dp.callback_query_handler(state=MuqriyVideoStates.qadamjolar_videos)
# async def qadamjolar_videos_state(call: types.CallbackQuery, state: FSMContext):
#     await call.message.delete()
#     data = await state.get_data()
#     c = data['c']
#     counter = data['counter']
#
#     datas = list(chunks(ITEMS, 15))
#
#     keys = await key_returner(
#         items=datas[c],
#         current_page=counter,
#         all_pages=len(datas)
#     )
#     first_index = datas[c][0] - 1
#     last_index = datas[c][-1]
#     text = str()
#     for i in MENU_POST[first_index:last_index]:
#         text += f"{i}"
#     await call.message.answer(
#         text=text,
#         reply_markup=keys
#     )
#     await MuqriyVideoStates.qadamjolar_menu.set()
