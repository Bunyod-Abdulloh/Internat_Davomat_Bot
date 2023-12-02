from aiogram.dispatcher.filters.state import StatesGroup, State


class Educators_State(StatesGroup):
    firstname = State()
    lastname = State()
    surname = State()
    first_number = State()
    second_number = State()
    check_second_number = State()
    work_days = State()
