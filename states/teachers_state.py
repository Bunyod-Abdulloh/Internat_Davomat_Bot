from aiogram.dispatcher.filters.state import StatesGroup, State


class TeacherForm(StatesGroup):
    fullname = State()
    select_class = State()
    first_phone = State()
    second_phone = State()
    check_second_phone = State()


class TeacherAttendance(StatesGroup):
    main = State()
