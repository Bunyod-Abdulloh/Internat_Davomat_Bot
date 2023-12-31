from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db

primary_classes = ["Matematika", "Alifbe", "Yozuv", "DG", "Tarbiya", "Ingliz tili", "Informatika", "Tasviriy san'at",
                   "JT", "Sinf soati", "Science", "Texnologiya", "Musiqa", "Математика", "Азбука", "Технология",
                   "Письмо", "Информатика", "Анг.язык", "Физ-ра", "ЛГ", "Кл.час", "ИЗО", "Воспитания", "Музыка",
                   "O'qish", "Ona tili", "Rus tili", "Tarbiya", "Чтение", "Русс.язык", "Узб.язык"]

senior_classes_uz = ["Texnologiya", "Tarbiya", "Musiqa", "Geografiya", "Botanika", "JT", "Tarix", "Ingliz tili",
                     "Matematika", "Ona tili", "DG", "Rus tili", "Informatika", "Tasviriy san'at", "Sinf soati",
                     "Adabiyot"]

senior_classes_ru = ["Литература", "Информатика", "Англ.язык", "Математика", "Ботаника", "Физ-ра", "Узб.язык"]


select_language_teachers = InlineKeyboardMarkup(row_width=1)
select_language_teachers.row(
    InlineKeyboardButton(
        text="O'zbek", callback_data="uz_teach"
    ),
    InlineKeyboardButton(
        text="Русский", callback_data="ru_teach"
    )
)


async def senior_lessons_ibutton(back_step: str, next_step: str,
                                 language_uz: bool = False, language_ru: bool = False):
    key = InlineKeyboardMarkup(row_width=2)
    lessons_uz = await db.get_lessons()

    if language_uz:
        for lesson in lessons_uz:
            key.insert(
                InlineKeyboardButton(
                    text=f"{lesson[0]} {lesson[2]}", callback_data=lesson[0]
                )
            )
    elif language_ru:
        for lesson in senior_classes_ru:
            key.insert(
                InlineKeyboardButton(
                    text=lesson, callback_data=lesson
                )
            )
    key.add(
        InlineKeyboardButton(
            text=f"⬅️ {back_step}", callback_data="backtib"
        ),
        InlineKeyboardButton(
            text=f"{next_step} ➡️", callback_data="nexttib"
        )
    )
    return key
