import random
import re
from aiogram import types, Dispatcher
from config import bot
from database.sql_commands import Database
from const import START_MENU_TEXT, START_MENU_FOR_ADMIN
from handlers.Transactions import start_fsm_send_money, load_name, load_amount, SendMoney
from handlers.friend_unfriend import (
    random_user_complain,
    friend_call,
    unfriend_call
)
from handlers.reference import create_reference_link, reference_list_menu, my_balance_menu
from keyboards.start_keyboard import start_menu_button, save_news_button, delete_my_favorite_news_button
from aiogram.utils.deep_linking import _create_link

from scraping.news_kg import NewsScraper


async def start(message: types.Message):
    telegram = Database().sql_select_admin_list()
    token = message.get_full_command()
    result = tuple(d['admin_tg_id'] for d in telegram)
    if message.from_user.id in result:
        with open(r"C:\Users\denis\PycharmProjects\hw1_month3\media\images.png", "rb") as photo:
            await bot.send_photo(
                chat_id=message.from_user.id,
                photo=photo,
                caption=START_MENU_FOR_ADMIN,
                reply_markup=await start_menu_button()
            )
    else:
        with open(r"C:\Users\denis\PycharmProjects\hw1_month3\media\images.png", "rb") as photo:
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=photo,
                caption=START_MENU_TEXT,
                reply_markup=await start_menu_button()
            )
    if token[1]:
        link = await _create_link(link_type='start', payload=token[1])
        telegram_id = Database().sql_select_owner_user_by_link(
            link=link
        )
        existed_reference = Database().sql_select_reference_tg_id(referral_telegram_id=message.from_user.id)
        if existed_reference:
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Вы уже есть в списке рефералов!')
        else:
            Database().sql_insert_reference_list(
                owner_tg_id=telegram_id[0]['telegram_id'],
                reference_tg_id=message.from_user.id
            )
            Database().insert_table(
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                firstname=message.from_user.first_name,
                lastname=message.from_user.last_name,
            )
            existed_balance = Database().select_existing_balance(telegram_id=telegram_id[0]['telegram_id'])
            if existed_balance:
                Database().update_balance(telegram_id=telegram_id[0]['telegram_id'])
            else:
                Database().sql_insert_into_balance(telegram_id=telegram_id[0]['telegram_id'],
                                                   balance=100)


async def last_news_call(call: types.CallbackQuery):
    scraper = NewsScraper()
    urls = scraper.parse_data()
    for url in urls:
        Database().sql_insert_news(
            news=url
        )
        news_id = Database().sql_select_news_id_by_link(
            news=url
        )
        await bot.send_message(chat_id=call.from_user.id,
                               text=url,
                               reply_markup=await save_news_button(
                                   id=news_id[0]['id']
                               ))

async def save_news_call(call: types.CallbackQuery):
    await bot.delete_message(
        chat_id=call.from_user.id,
        message_id=call.message.message_id
    )
    news_id = re.sub('save_news_','',call.data)
    favorite_news_link = Database().sql_select_news_link_by_id(
        id=news_id
    )
    Database().sql_insert_favorite_news(
        telegram_id=call.from_user.id,
        favorite_news=favorite_news_link[0]['news']
    )

async def my_news_call(call: types.CallbackQuery):
    my_news = Database().sql_select_favorite_news_by_own_id(
        telegram_id=call.from_user.id
    )
    for my_new in my_news:
        id_links = Database().sql_select_my_favorite_news_id_by_link(
            link=my_new['favorite_news']
        )
        await bot.send_message(
            chat_id=call.from_user.id,
            text=my_new['favorite_news'],
            reply_markup= await delete_my_favorite_news_button(
                id= id_links[0]['id']
            )
        )

async def delete_favorite_news_call(call: types.CallbackQuery):
    news_id = re.sub('deletefavorite_news_', '', call.data)
    Database().sql_delete_from_favorite_news(
        id=int(news_id)
    )
    await bot.delete_message(
        chat_id=call.from_user.id,
        message_id=call.message.message_id
    )




def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_callback_query_handler(random_user_complain, lambda call: call.data == 'play_game')
    dp.register_callback_query_handler(friend_call, lambda call: call.data.startswith('friend_button_'))
    dp.register_callback_query_handler(unfriend_call, lambda call: call.data.startswith('unfriend_button'))
    dp.register_callback_query_handler(create_reference_link, lambda call: call.data == 'reference_link')
    dp.register_callback_query_handler(reference_list_menu, lambda call: call.data == 'list_referral')
    dp.register_callback_query_handler(my_balance_menu, lambda call: call.data == 'my_balance')
    dp.register_callback_query_handler(start_fsm_send_money, lambda call: call.data == 'money')
    dp.register_message_handler(load_name, content_types=['text'], state=SendMoney.name_user)
    dp.register_message_handler(load_amount, content_types=['text'], state=SendMoney.amount)
    dp.register_callback_query_handler(last_news_call, lambda call: call.data == 'last_news')
    dp.register_callback_query_handler(save_news_call, lambda call: call.data.startswith('save_news_'))
    dp.register_callback_query_handler(my_news_call,lambda call: call.data == 'my_news')
    dp.register_callback_query_handler(delete_favorite_news_call,lambda call: call.data.startswith('deletefavorite_news_'))
