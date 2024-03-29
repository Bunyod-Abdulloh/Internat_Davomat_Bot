import middlewares, filters, handlers

from aiogram import executor

from handlers.admin.an_scheduler import scheduler
from loader import dp, db
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await db.create()
    # await db.drop_table_attendance()
    # await db.drop_table_checker()
    # await db.drop_table_students()
    # await db.drop_table_employees()
    await db.create_table_checker()
    await db.create_table_attendance()
    await db.create_table_students()
    await db.create_table_employees()

    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)

    # scheduler.start()


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
