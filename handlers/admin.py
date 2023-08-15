from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from config import bot
from database.sql_commands import Database
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import AdminPollId


async def secret_word_admin(message: types.Message):
    if message.from_user.id == 664999418:
        await bot.delete_message(chat_id=message.chat.id,
                                 message_id=message.message_id
                                 )
        await bot.send_message(chat_id=message.from_user.id,
                               text='WELCOME ADMIN',
                               reply_markup=await admin_users_list_button())


async def admin_users_list_button():
    markup = InlineKeyboardMarkup()
    users_list = InlineKeyboardButton('Список пользователей',
                                      callback_data='admin_users_list')
    potential_ban_users = InlineKeyboardButton('Cписок потенциальных банов',
                                               callback_data='admin_potential_ban')
    markup.row(
        users_list,
        potential_ban_users
    )
    return markup


async def admin_users_list(call: types.CallbackQuery):
    users = Database().select_users_for_admin()
    list_of_users = []
    for user in users:
        if not user['username']:
            list_of_users.append(f"[{user['firstname']}](tg://user?id={user['telegram_id']})")
        else:
            list_of_users.append(f"[{user['username']}](tg://user?id={user['telegram_id']})")

    list_of_users = "\n".join(list_of_users)
    await call.message.reply(text=list_of_users,
                             parse_mode=types.ParseMode.MARKDOWN)


async def send_message_to_users_button():
    markup = InlineKeyboardMarkup()
    send_to_users = InlineKeyboardButton('Отправить всем пользователям предупреждение',
                                         callback_data='send_warning')
    markup.row(
        send_to_users
    )
    return markup


async def admin_potential_ban_users(call: types.CallbackQuery):
    potential_bans = Database().select_potential_ban_users()
    list_of_potential_ban = []
    if potential_bans:
        for potential_ban in potential_bans:
            if not potential_ban['username']:
                list_of_potential_ban.append(
                    f"[{potential_ban['firstname']}](tg://user?id={potential_ban['telegram_id']}) Нарушений :{potential_ban['Bancount']}  ")
            else:
                list_of_potential_ban.append(
                    f"[{potential_ban['username']}](tg://user?id={potential_ban['telegram_id']}) Нарушений : {potential_ban['Bancount']}  ")
        list_of_potential_ban = '\n'.join(list_of_potential_ban)
        await call.message.reply(text=list_of_potential_ban,
                                 parse_mode=types.ParseMode.MARKDOWN,
                                 reply_markup=await send_message_to_users_button()
                                 )
    else:
        await call.message.reply(text=f'Нету пользователей с потенциальным баном!')


async def send_message_to_users(call: types.CallbackQuery):
    warning = Database().select_all_users()
    for warn in warning:
        ban_count = Database().select_users_counts(telegram_id=warn['telegram_id'])
        await call.bot.send_message(chat_id=warn['telegram_id'],
                                    text=f'У вас {ban_count[0]} предупреждений')


async def get_all_poll_answers_id(message: types.Message):
    if message.from_user.id == 664999418:
        await AdminPollId.id.set()
        poll_id = Database().sql_select_all_poll_answers_id()
        id_list = []
        for id in poll_id:
            id_list.append(f"POLL ID: {id['id']}")
        id_list = '\n'.join(id_list)
        await bot.send_message(chat_id=message.from_user.id,
                               text=id_list)
        await message.reply('Выберите ID опроса, для получения'
                            '\nполной информации об опросе!')

async def load_id(message: types.Message,state: FSMContext):
    if isinstance(int(message.text),int):
        async with state.proxy() as data:
            data['id'] = message.text
            poll_answers = Database().sql_select_poll_answers_by_id(id=data['id'])
            await bot.send_message(chat_id=message.from_user.id,
                             text=f"ID: {poll_answers[0]['id']}"
                                  f"\nIDEA: {poll_answers[0]['idea']}"
                                  f"\nPROBLEMS: {poll_answers[0]['problems']}"
                                  f"\nTELEGRAM_ID: {poll_answers[0]['telegram_id']}")
            await state.finish()
    else:
        await message.reply('Введен неверный ID!')
        await state.finish()




def register_admin_handler(dp: Dispatcher):
    dp.register_message_handler(secret_word_admin, lambda word: 'admin' in word.text)
    dp.register_callback_query_handler(admin_users_list, lambda call: call.data == 'admin_users_list')
    dp.register_callback_query_handler(admin_potential_ban_users, lambda call: call.data == 'admin_potential_ban')
    dp.register_callback_query_handler(send_message_to_users, lambda call: call.data == 'send_warning')
    dp.register_message_handler(get_all_poll_answers_id,commands=['getpoll'])
    dp.register_message_handler(load_id,content_types=['text'],state=AdminPollId.id)
