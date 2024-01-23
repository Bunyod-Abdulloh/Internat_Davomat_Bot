from aiogram.dispatcher.filters.state import StatesGroup, State


class EducatorForm(StatesGroup):
    fullname = State()
    first_number = State()
    second_number = State()
    check_second_number = State()
    select_class = State()


class EducatorsMorning(StatesGroup):
    main = State()
    attendance = State()
    first_class = State()


class EducatorsDiurnal(StatesGroup):
    main = State()
    attendance = State()


class EducatorsAnotherClass(StatesGroup):
    main = State()
