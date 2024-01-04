from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.default.main_menu_cbuttons import main_menu_uz
from keyboards.inline.admin_inline_keys import admin_check_btn
from keyboards.inline.educators_inline_keys import (edu_phone_number, edu_work_time, educators_class_btn,
                                                    educators_main_uz)
from loader import dp, db, bot
from states.educators_states import EducatorsQuestionnaire, EducatorsWorkTime, EducatorsMain


# e_m = Educators_main (handlers/educators/file-name)
@dp.message_handler(text='🧑‍🏫 Tarbiyachi', state='*')
async def em_main(message: types.Message):
    educator = await db.select_educator(telegram_id=message.from_user.id)

    if not educator:
        await message.answer(
            text="O'zingizga biriktirilgan sinf yoki sinflarni tanlang:", reply_markup=await educators_class_btn()
        )
        await EducatorsQuestionnaire.select_class.set()
    else:
        await message.answer(
            text="Tugmalardan birini tanlang:", reply_markup=educators_main_uz
        )

        # current_hour = datetime.now().hour

        # if current_hour >= 6:
        #     if current_hour < 10:
        #         if len(educator) == 1:
        # class_number = educator[0][4]
        # get_morning = await db.get_students(
        #     class_number=class_number
        # )
        # absent = await db.count_morning_check(class_number=class_number, morning_check="✅")
        # present = await db.count_morning_check(class_number=class_number, morning_check="🔘")
        # explicable = await db.count_morning_check(class_number=class_number, morning_check="🟡")
        # await call.message.edit_text(
        #     text="O'quvchilarni kelgan kelmaganligini tugmalarni bosib belgilang va yakunda <b>☑️ Tasdiqlash</b> "
        #          "tugmasini bosing!"
        #          "\n\n✅ - Kelganlar\n🔘 - Sababli kelmaganlar\n🟡 - Sababsiz kelmaganlar",
        #     reply_markup=await view_students_uz(
        #         work_time=get_morning, class_number=class_number, back="Ortga", check="Tasdiqlash",
        #         absent=f"✅ : {absent} ta", explicable=f"🟡 : {explicable} ta", present=f"🔘 : {present} ta", uz=True
        #     )
        # )
        # await EducatorsWorkTime.morning.set()
                    # await call.message.edit_text(
                    #     text="Salom", reply_markup=await view_students_uz(
                    #         work_time=
                    #     )
                    # )
            # else:
            #     if len(educator) == 1:
            #         print(educator)
        # else:
        #     print("Hozirgi vaqt 06:00 gacha.")


@dp.callback_query_handler(state=EducatorsQuestionnaire.select_class)
async def e_m_select_class(call: types.CallbackQuery, state: FSMContext):
    select_educator = await db.select_educator(telegram_id=call.from_user.id)

    if call.data == "eduback_one":
        await call.message.edit_text(
            text="Bosh sahifa", reply_markup=main_menu_uz
        )
        await state.finish()

    elif call.data == "educontinue":
        await call.message.edit_text(
            text="Ism, familiya va otangizni ismini kiriting:\n\n<b>Namuna: Djalilov Zoir Saydirahmon o'g'li</b>"
        )
        await EducatorsQuestionnaire.fullname.set()
    else:
        educator = await db.select_educator_mark(telegram_id=call.from_user.id, class_number=call.data)
        print(f"{call.data} 79")
        if educator is None:
            await db.add_educator_new(
                telegram_id=call.from_user.id, mark="✅", class_number=call.data
            )
        else:
            if educator[0] == "✅":
                await db.update_educator_mark(
                    mark="🔘", telegram_id=call.from_user.id, class_number=call.data
                )
            else:
                await db.update_educator_mark(
                    mark="✅", telegram_id=call.from_user.id, class_number=call.data
                )
        await call.message.edit_text(
            text="O'zingizga biriktirilgan sinf yoki sinflarni tanlang:", reply_markup=await educators_class_btn()
        )


@dp.message_handler(state=EducatorsQuestionnaire.fullname)
async def em_get_fullname(message: types.Message):
    await db.update_educator_fullname(
        fullname=message.text, telegram_id=message.from_user.id
    )
    await message.answer(
        text="Telefon raqamingizni kiriting:\n\n<b>Namuna: 998974450292</b>"
    )
    await EducatorsQuestionnaire.first_number.set()


@dp.message_handler(state=EducatorsQuestionnaire.first_number)
async def educators_get_first_number(message: types.Message):
    if message.text.isdigit():
        await db.update_educator_first_phone(first_phone=f"+{message.text}", telegram_id=message.from_user.id)

        await message.answer(
            text="Agar raqamingiz ikkita bo'lsa <b><i>Raqam kiritish</i></b> tugmasini, bitta bo'lsa "
                 "<b><i>Raqamim bitta</i></b> tugmasini bosing!",
            reply_markup=edu_phone_number
        )
        await EducatorsQuestionnaire.second_number.set()
    else:
        await message.answer(
            text="Iltimos faqat raqam kiriting"
        )


@dp.callback_query_handler(state=EducatorsQuestionnaire.second_number)
async def educators_get_second_number(call: types.CallbackQuery, state: FSMContext):
    if call.data == "add_edusecond_number":
        await call.message.edit_text(
            text="Ikkinchi raqamingizni kiriting:\n\n<b>Namuna: 998974450292</b>"
        )
        await EducatorsQuestionnaire.check_second_number.set()

    elif call.data == "edu_number_first":
        await call.message.edit_text(
            text="Ma'lumotlaringiz qabul qilindi! Admin ma'lumotlaringizni tasdiqlaganidan so'ng botdan "
                 "foydalanishingiz mumkin!"
        )
        educator = await db.select_educator(telegram_id=call.from_user.id)

        sinf = str()

        for classes in educator:
            sinf += f"{classes[4]} "

        datas = await db.select_educator_distinct(telegram_id=call.from_user.id)

        for admin in ADMINS:
            await bot.send_message(
                chat_id=admin,
                text=f"Yangi hodim ma'lumotlari qabul qilindi!"
                     f"\n\nLavozim: Tarbiyachi"
                     f"\n\nF.I.SH: {datas[1]}"
                     f"\n\nTelefon raqam: {datas[2]}"
                     f"\n\nSinf: {sinf}",
                disable_web_page_preview=False,
                reply_markup=await admin_check_btn(
                    user_id=call.from_user.id
                )
            )
        sinf = str()


@dp.message_handler(state=EducatorsQuestionnaire.check_second_number)
async def educators_check_second_number(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await db.update_educator_second_phone(
            second_phone=f"+{message.text}", telegram_id=message.from_user.id
        )
        await message.edit_text(
            text="O'zingizga biriktirilgan sinf yoki sinflarni tanlang:", reply_markup=await educators_class_btn()
        )
        await state.update_data(
            counter_educator=0
        )
        await EducatorsQuestionnaire.select_class.set()
    else:
        await message.answer(
            text="Iltimos, faqat raqam kiriting!"
        )


# @dp.callback_query_handler(state=EducatorsQuestionnaire.select_class)
# async def e_m_select_class(call: types.CallbackQuery, state: FSMContext):
#     # select_educator = await db.select_educator_(telegram_id=call.from_user.id, class_number=call.data)
#
#     if call.data == "eduback_one":
#         await call.message.edit_text(
#             text="Bosh sahifa", reply_markup=main_menu_uz
#         )
#         await state.finish()
#
#     elif call.data == "educontinue":
#         pass
#
#     else:
#         data = await state.get_data()
#         count = data['counter_educator']
#         educator = await db.select_educator_(telegram_id=call.from_user.id, class_number=call.data)
#         count += 1
#
#         print(educator)
#         if educator is None:
#             await db.add_educators_class(class_number=call.data, telegram_id=call.from_user.id)
        # if not select_educator:
        #     await db.add_educator_(
        #         telegram_id=call.from_user.id, class_number=call.data
        #     )
        #     await state.update_data(
        #         educator_class_number=call.data
        #     )
        #     await call.message.edit_text(
        #         text="Ism, familiya va otangizni ismini kiriting:"
        #              "\n\n<b>Namuna: Djalilov Zoir Saydirahmon o'g'li</b>"
        #     )
        #     await EducatorsQuestionnaire.fullname.set()
        # else:
        #     if select_educator[-1] is False:
        #         await call.answer(
        #             text="Ma'lumotlaringiz hali admin tomonidan tasdiqlanmadi!", show_alert=True
        #         )
        #     else:
        #         await call.message.edit_text(
        #             text="Kerakli bo'limni tanlang:", reply_markup=await select_chapters_educator(
        #                 uz=True, class_number=call.data, back="Ortga"
        #             )
        #         )
        #         await EducatorsMain.main.set()


# await call.message.edit_text(
#     text="Ism, familiya va otangizni ismini kiriting:"
#          "\n\n<b>Namuna: Djalilov Zoir Saydirahmon o'g'li</b>"
# )
# await EducatorsQuestionnaire.fullname.set()


@dp.callback_query_handler(state=EducatorsMain.main)
async def esm_main(call: types.CallbackQuery):
    print(call.data)
    if call.data == "back_chapters":
        await call.message.edit_text(
            text="O'zingizga biriktirilgan sinfni tanlang:", reply_markup=await educators_class_btn()
        )
        await EducatorsQuestionnaire.select_class.set()

    if call.data.__contains__("presents_"):
        await call.message.edit_text(
            text="Ish vaqtingizni tanlang:", reply_markup=await edu_work_time(
                class_number=call.data, morning="Ertalabki", half_day="Yarim kun",
                all_day="To'liq kun", back="Ortga"
            )
        )
        await EducatorsWorkTime.presents.set()
    elif call.data.__contains__("cabineteducator_"):
        pass
