from aiogram.dispatcher.filters.state import StatesGroup, State


class Educators_State(StatesGroup):
    fullname = State()
    first_number = State()
    second_number = State()
    check_second_number = State()
    select_class = State()
