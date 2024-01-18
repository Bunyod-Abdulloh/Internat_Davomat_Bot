import pytz

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from data.config import ADMINS
from loader import bot, db

tz = pytz.timezone('Asia/Tashkent')

job_defaults = {
    "misfire_grace_time": 3600
}

jobstores = {
    "default": SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}

scheduler = AsyncIOScheduler(timezone=tz, jobstores=jobstores, job_defaults=job_defaults)


async def update_all_attendance_job():
    await db.update_employee_all_attendance(attendance=True)
    # await bot.send_message(chat_id=ADMINS[0],
    #                        text="Ertalabki tarbiyachilar bo'limi yoqildi!"
    #                        )


async def morning_off_mon_sat():
    await db.update_educators_morning(morning=False)
    await bot.send_message(chat_id=ADMINS[0],
                           text="Ertalabki tarbiyachilar bo'limi yopildi!"
                           )


async def day_on_mon_sat():
    await db.update_educators_day(day=True)
    await bot.send_message(chat_id=ADMINS[0],
                           text="Kunduzgi tarbiyachilar bo'limi yoqildi!"
                           )


async def day_off_mon_fri():
    await db.update_educators_day(day=False)
    await bot.send_message(chat_id=ADMINS[0],
                           text="Kunduzgi tarbiyachilar bo'limi yopildi!"
                           )


async def all_off():
    await db.update_educators_morning(morning=False)
    await db.update_educators_day(day=False)
    await bot.send_message(chat_id=ADMINS[0],
                           text="Tarbiyachilar uchun barcha bo'limlar yopildi!")


scheduler.add_job(update_all_attendance_job, trigger='cron', day_of_week='mon-sat', hour=13, minute=20)
# scheduler.add_job(morning_off_mon_sat, trigger='cron', day_of_week='mon-sat', hour=9, minute=45)
# scheduler.add_job(day_on_mon_sat, trigger='cron', day_of_week='mon-sat', hour=12, minute=0)
# scheduler.add_job(day_off_mon_fri, trigger='cron', day_of_week='mon-fri', hour=20, minute=0)
# scheduler.add_job(all_off, trigger='cron', day_of_week='sat', hour=17, minute=0)
