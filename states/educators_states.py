from aiogram.dispatcher.filters.state import StatesGroup, State


class EducatorsQuestionnaire(StatesGroup):
    fullname = State()
    first_number = State()
    second_number = State()
    check_second_number = State()
    select_class = State()


class EducatorsMain(StatesGroup):
    main = State()


class EducatorsMorning(StatesGroup):
    main = State()
    attendance = State()


class EducatorsDiurnal(StatesGroup):
    main = State()
    attendance = State()


class EducatorsWorkTime(StatesGroup):
    main = State()
    presents = State()
    morning = State()
    day = State()
    up_to_four = State()
    after_four = State()
