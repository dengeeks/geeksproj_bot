from aiogram.utils import executor
from config import dp
from handlers import start
from database.sql_commands import Database


async def on_start_up(_):
    db = Database()
    db.create_table()

start.register_start_handlers(dp=dp)


if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_start_up)