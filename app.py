from aiogram import executor

from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await db.create()
    # await db.drop_table_educators()
    await db.drop_table_students()
    await db.create_table_educators()
    await db.create_table_students()
    # for n in range(50):
    #     await db.add_educators(123456789 + n)
    # await db.add_student(class_number="6-V",
    #                      fullname="Abdulxayev Muhammadzohir")
    # await db.add_student(class_number="6-V",
    #                      fullname="Abdulxayev Firdavs")

    await set_default_commands(dispatcher)

    await on_startup_notify(dispatcher)

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
