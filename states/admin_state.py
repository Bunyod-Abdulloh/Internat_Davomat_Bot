from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminEducator_State(StatesGroup):
    cancel_message = State()
    cancel_check = State()


class AdminEditEdicators(StatesGroup):
    main = State()
    edit_fullname = State()
    check_fullname = State()


class AdminMain(StatesGroup):
    parents = State()
    curators = State()
    educators = State()
    students = State()


class AdminStudents(StatesGroup):
    add_class = State()
    delete_class = State()
    add_students = State()
    delete_students = State()
    add_student = State()
    delete_student = State()
    students_xls = State()
    download_xls = State()
