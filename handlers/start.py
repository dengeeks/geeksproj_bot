
from aiogram import types,Dispatcher
from config import bot
from database.sql_commands import Database
from const import START_MENU_TEXT,START_MENU_FOR_ADMIN

async def start_button(message: types.Message):
    telegram = Database().sql_select_admin_list()
    result = tuple(d['admin_tg_id'] for d in telegram)
    if message.from_user.id in result:
        with open(r"C:\Users\denis\PycharmProjects\hw1_month3\media\images.png", "rb") as photo:
            await bot.send_photo(
                chat_id=message.from_user.id,
                photo=photo,
                caption=START_MENU_FOR_ADMIN
            )
    else:
        Database().insert_table(
        telegram_id= message.from_user.id,
        username= message.from_user.username,
        firstname= message.from_user.first_name,
        lastname= message.from_user.last_name,
        )
        with open(r"C:\Users\denis\PycharmProjects\hw1_month3\media\images.png","rb") as photo:
            await bot.send_photo(
                chat_id=message.chat.id,
                photo = photo,
                caption=START_MENU_TEXT
            )


def register_start_handlers(dp : Dispatcher):
    dp.register_message_handler(start_button,commands=['start'])
