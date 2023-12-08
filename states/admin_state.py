from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminEducator_State(StatesGroup):
    cancel_message = State()
    cancel_check = State()


class AdminEditEdicators(StatesGroup):
    main = State()
    edit_fullname = State()
    check_fullname = State()
