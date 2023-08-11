
from aiogram import types,Dispatcher
from config import bot
from database.sql_commands import Database

async def start_button(message: types.Message):
    print(message)
    Database().insert_table(
    telegram_id= message.from_user.id,
    username= message.from_user.username,
    firstname= message.from_user.first_name,
    lastname= message.from_user.last_name,
    )
    await message.reply(text=f'HEEELLLOO {message.from_user.first_name}')



def register_start_handlers(dp : Dispatcher):
    dp.register_message_handler(start_button,commands=['start'])