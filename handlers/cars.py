from aiogram import types, Dispatcher
from config import bot
from database.sql_commands import Database
from scraping.cars import CarsScraping


async def list_cars(message: types.Message):
    scraper = CarsScraping()
    urls = await scraper.parse_data()
    for url in urls:
        await bot.send_message(chat_id=message.from_user.id,
                                text=url)


def register_cars_handlers(dp: Dispatcher):
    dp.register_message_handler(list_cars,commands=['cars'])
