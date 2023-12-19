from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

primary_classes = ["Matematika", "Alifbe", "Yozuv", "DG", "Tarbiya", "Ingliz tili", "Informatika", "Tasviriy san'at",
                   "JT", "Sinf soati", "Science", "Texnologiya", "Musiqa", "Математика", "Азбука", "Технология",
                   "Письмо", "Информатика", "Анг.язык", "Физ-ра", "ЛГ", "Кл.час", "ИЗО", "Воспитания", "Музыка",
                   "O'qish", "Ona tili", "Rus tili", "Tarbiya", "Чтение", "Русс.язык", "Узб.язык"]

senior_classes = ["Texnologiya", "Tarbiya", "Musiqa", "Geografiya", "Botanika", "JT", "Tarix", "Ingliz tili",
                  "Matematika", "Ona tili", "DG", "Rus tili", "Informatika", "Tasviriy san'at", "Sinf soati",
                  "Adabiyot", "Литература", "Информатика", "Англ.язык", "Математика", "Ботаника", "Физ-ра", "Узб.язык"]


async def senior_lessons_ibutton(back_step: str, next_step: str):
    key = InlineKeyboardMarkup(row_width=2)
    for lesson in senior_classes:
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
            text=f"➡️ {next_step}", callback_data="nexttib"
        )
    )
    return key
