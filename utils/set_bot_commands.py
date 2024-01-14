from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand(command="/start", description="Botni qayta ishga tushirish"),
            types.BotCommand(command="/new_employees", description="Yangi foydalanuvchi"),
            types.BotCommand(command="/admins", description="Adminlar bo'limi"),
            types.BotCommand(command="/help", description="Yordam")
        ]
    )
