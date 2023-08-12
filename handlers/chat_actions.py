import datetime

from aiogram import types,Dispatcher
from config import bot
from database.sql_commands import Database

async def ban_on_words(message: types.Message):
    ban_words = ['fuck','bitch','ass','dickhead','shit']
    if message.chat.id == -1001977728039:
        for ban_word in ban_words:
            if ban_word in message.text.lower().replace(" ",""):
                await bot.delete_message(
                    chat_id=message.chat.id,
                    message_id=message.message_id
                )
                existing= Database().select_users_ban(telegram_id= message.from_user.id)
                if existing:
                    Database().update_ban_users_count(telegram_id=message.from_user.id)
                else:
                    Database().insert_ban_users_count(
                        telegram_id=message.from_user.id,
                        bancount=1)
                counts = Database().select_users_counts(telegram_id=message.from_user.id)
                await bot.send_message(chat_id=message.chat.id,
                                       text=f'Ваше {counts[0]} предупреждение'
                                       )
                if counts[0] == 3:
                    ban_time = datetime.timedelta(minutes=1)
                    await bot.ban_chat_member(
                        chat_id=message.chat.id,
                        user_id=message.from_user.id,
                        until_date=ban_time
                    )
                    await bot.send_message(chat_id=message.chat.id,
                                     text=f"Пользователь {message.from_user.username}"
                                          f"\nбыл забанен на {ban_time}")
                    Database().delete_banned_users(
                        telegram_id=message.from_user.id
                    )



def register_chat_handler(dp: Dispatcher):
    dp.register_message_handler(ban_on_words)