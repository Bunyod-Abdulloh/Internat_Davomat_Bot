import middlewares, filters, handlers

from aiogram import executor

from handlers.admin.an_scheduler import scheduler
from keyboards.inline.all_inline_keys import classes_list
from loader import dp, db
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await db.create()
    await db.drop_table_educators()
    # await db.drop_table_students()
    # await db.drop_table_teachers()
    # await db.drop_table_lessons()
    # await db.drop_table_admins()
    # await db.create_table_admins()
    # await db.create_table_classes()
    await db.create_table_educators()
    await db.create_table_students()
    # await db.create_table_teachers()
    # await db.create_table_lessons()
    for sinf in classes_list:
        await db.add_educators_class(
            class_number=sinf
        )
    # await db.add_admin(telegram_id=1041847396)

    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)

    # scheduler.start()


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
