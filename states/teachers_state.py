from aiogram.dispatcher.filters.state import StatesGroup, State


class TeachersAnketa(StatesGroup):
    get_fullname = State()
    get_lesson = State()
    get_work_days = State()
