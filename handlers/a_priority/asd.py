from datetime import datetime

from aiogram import types


async def get_work_time(current_hour: int):
    morning = [6, 7, 8, 9, 10, 11]
    day = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

    if current_hour in morning:
        return str('morning')
    elif current_hour in day:
        return str('day')
