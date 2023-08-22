from aiogram import types, Dispatcher
from config import bot
from database.sql_commands import Database
from keyboards.start_keyboard import friend_unfriend_button
import re
import random


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



async def unfriend_call(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.message.chat.id,
                             message_id=call.message.message_id)
    await random_user_complain(call=call)



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