from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminEducator_State(StatesGroup):
    cancel_message = State()
    cancel_check = State()
