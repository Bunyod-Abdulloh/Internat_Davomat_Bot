from apscheduler.schedulers.asyncio import AsyncIOScheduler

from data.config import ADMINS
from loader import bot


async def job_function():
    # await bot.send_message(
    #     chat_id=ADMINS[0],
    #     text="Salom Python"
    # )
    print('Salom Aiogram!')

# Create a scheduler instance
scheduler = AsyncIOScheduler()

# Schedule the job to run every 1 minute
scheduler.add_job(job_function, 'cron', day_of_week='*', hour=12, minute=39)

# Start the scheduler
if __name__ == '__main__':
    scheduler.start()
