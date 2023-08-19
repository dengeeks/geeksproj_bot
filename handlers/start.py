import random
import re
from aiogram import types, Dispatcher
from config import bot
from database.sql_commands import Database
from const import START_MENU_TEXT, START_MENU_FOR_ADMIN
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def unfriend_call(call: types.Message):
    await bot.delete_message(chat_id=call.message.chat.id,
                             message_id=call.message.message_id)
    await random_user_complain(call=call)



async def friend_unfriend_button(id):
    markup = InlineKeyboardMarkup()
    friend_button = InlineKeyboardButton('Друг👍🏻',
                                         callback_data=f'friend_button_{id}')
    unfriend_button = InlineKeyboardButton('Недруг👎🏻',
                                           callback_data='unfriend_button')
    markup.row(friend_button, unfriend_button)
    return markup


async def play_game_button():
    markup = InlineKeyboardMarkup()
    play_game = InlineKeyboardButton('Сыграем игру Друг👍🏻-Недруг?👎🏻',
                                     callback_data='play_game')
    markup.row(play_game)
    return markup


async def random_user_complain(call: types.CallbackQuery):
    users_complain_list = Database().sql_select_all_user_complain()
    random_user_form = random.choice(users_complain_list)
    await bot.send_message(chat_id=call.message.chat.id,
                           text=f'*ID*: {random_user_form["ID"]}\n'
                                f'*Complainer*: {random_user_form["who_complained"]}\n'
                                f'*ID_complained_user*: {random_user_form["tg_id_complained_user"]}\n'
                                f'*ID_bad_user*: {random_user_form["tg_id_bad_user"]}\n'
                                f'*Reason*: {random_user_form["reason"]}\n'
                                f'*Count*: {random_user_form["count"]}',
                           parse_mode=types.ParseMode.MARKDOWN,
                           reply_markup=await friend_unfriend_button(id=random_user_form['ID']))

async def friend_call(call: types.CallbackQuery):
    owner_id = re.sub("friend_button_", "", call.data)
    friended_form = Database().sql_select_already_friend(
        owner_id=owner_id,
        friended_tg_id=call.from_user.id
    )
    if friended_form:
        await bot.send_message(
            chat_id=call.message.chat.id,
            text='Вы уже подружились с ним🫂'
        )
        await bot.delete_message(chat_id=call.message.chat.id,
                                 message_id=call.message.message_id)
        await random_user_complain(call=call)
    else:
        Database().sql_insert_already_friend(
            owner_id=owner_id,
            friended_tg_id=call.from_user.id
        )
        Database().update_report_count_by_friend(ID=owner_id)
        Database().delete_user_complain()
        await call.message.reply('Данному пользователю снялась жалоба'
                                 '\nна 1 единицу🙌🙌')
        await bot.delete_message(chat_id=call.message.chat.id,
                                 message_id=call.message.message_id)
        await random_user_complain(call=call)

        


async def start_button(message: types.Message):
    telegram = Database().sql_select_admin_list()
    result = tuple(d['admin_tg_id'] for d in telegram)
    if message.from_user.id in result:
        with open(r"C:\Users\denis\PycharmProjects\hw1_month3\media\images.png", "rb") as photo:
            await bot.send_photo(
                chat_id=message.from_user.id,
                photo=photo,
                caption=START_MENU_FOR_ADMIN,
                reply_markup=await play_game_button()
            )
    else:
        Database().insert_table(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            firstname=message.from_user.first_name,
            lastname=message.from_user.last_name,
        )
        with open(r"C:\Users\denis\PycharmProjects\hw1_month3\media\images.png", "rb") as photo:
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=photo,
                caption=START_MENU_TEXT,
                reply_markup=await play_game_button()
            )


def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(start_button, commands=['start'])
    dp.register_callback_query_handler(random_user_complain, lambda call: call.data == 'play_game')
    dp.register_callback_query_handler(friend_call,lambda call: call.data.startswith('friend_button_'))
    dp.register_callback_query_handler(unfriend_call,lambda call: call.data.startswith('unfriend_button'))
