import datetime
import re
from aiogram.dispatcher import FSMContext
from config import bot
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from aiogram import types, Dispatcher
from database.sql_commands import Database
from aiogram.dispatcher.filters.state import State, StatesGroup
from database.sql_commands import Database


class ReportUser(StatesGroup):
    report = State()
    reason = State()

class Username(StatesGroup):
    username = State()




async def report_message_button():
    markup = InlineKeyboardMarkup()
    chance_button = InlineKeyboardButton('Возможность',
                                         callback_data='chance')
    pass_button = InlineKeyboardButton('Пропустить',
                                       callback_data='pass_button')
    markup.row(chance_button,
               pass_button)
    return markup


async def start_report_fsm(message: types.Message):
    await bot.delete_message(chat_id=message.chat.id,
                             message_id=message.message_id)
    await bot.send_message(chat_id=message.chat.id,
                           text='Введите @username  или firstname пользователя,'
                                '\nчтобы отправить жалобу')
    await ReportUser.report.set()



async def report_to_user(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        report_username = re.sub("@","", message.text)
        data['report'] = report_username
        await bot.delete_message(chat_id=message.chat.id,
                                 message_id=message.message_id)
        await bot.send_message(chat_id=message.chat.id,
                               text='Введите причину жалобы')
        await ReportUser.reason.set()


async def load_reason(message: types.Message,state: FSMContext):
    await bot.delete_message(chat_id=message.chat.id,
                             message_id=message.message_id)
    async with state.proxy() as data:
        data['reason'] = message.text
    bad_user_id_by_firstname= await Database().sql_select_tg_user_by_firstname(firstname=data['report'])
    bad_user_id_by_username= await Database().sql_select_tg_user_by_username(username=data['report'])
    if bad_user_id_by_username:
        existing = await Database().sql_select_existing_bad_user(telegram_id_bad_user=bad_user_id_by_username[0]['telegram_id'])
        if existing:
            await Database().sql_update_user_complain(telegram_id_bad_user=bad_user_id_by_username[0]['telegram_id'])
            await bot.send_message(chat_id=message.chat.id,
                                   text='Ваша жалоба принята!')
            await state.finish()
        else:
            await Database().sql_insert_user_complain(username_first_who_complained=message.from_user.first_name,
                                                telegram_id_complained_user=message.from_user.id,
                                                telegram_id_bad_user=bad_user_id_by_username[0]['telegram_id'],
                                                reason=data['reason'],
                                                count=1)
            await message.reply('Ваша жалоба принята')
            await state.finish()
        counts = await Database().sql_select_report_count(bad_user_id_by_username[0]['telegram_id'])
        if counts[0]['report_count'] >= 3:
            ban_time = datetime.timedelta(minutes=1)
            await bot.ban_chat_member(
                chat_id=message.chat.id,
                user_id=bad_user_id_by_username[0]['telegram_id'],
                until_date=ban_time
            )
            await bot.send_message(chat_id=message.chat.id,
                                   text=f"Пользователь "
                                        f"\nбыл забанен на {ban_time}")
            await Database().sql_delete_reported_banned_users(bad_user_id_by_username[0]['telegram_id'])
        await bot.send_message(chat_id=bad_user_id_by_username[0]['telegram_id'],
                                text='На вас была отправлена жалоба!',
                               reply_markup= await report_message_button()
                                )
    else:
        await bot.send_message(chat_id=message.chat.id,
                               text='Вы ввели неверный @username или firstname')
        await state.finish()
    if bad_user_id_by_firstname:
        existing = await Database().sql_select_existing_bad_user(
            telegram_id_bad_user=bad_user_id_by_firstname[0]['telegram_id'])
        if existing:
            await Database().sql_update_user_complain(telegram_id_bad_user=bad_user_id_by_firstname[0]['telegram_id'])
            await bot.send_message(chat_id=message.chat.id,
                                   text='Ваша жалоба принята!')
            await state.finish()
        else:
            await Database().sql_insert_user_complain(username_first_who_complained=message.from_user.first_name,
                                                telegram_id_complained_user=message.from_user.id,
                                                telegram_id_bad_user=bad_user_id_by_firstname[0]['telegram_id'],
                                                reason=data['reason'],
                                                count=1)
            await message.reply('Ваша жалоба принята')
            await state.finish()
        counts = await Database().sql_select_report_count(bad_user_id_by_firstname[0]['telegram_id'])
        if counts[0]['report_count'] >= 3:
            ban_time = datetime.timedelta(minutes=1)
            await bot.ban_chat_member(
                chat_id=message.chat.id,
                user_id=bad_user_id_by_firstname[0]['telegram_id'],
                until_date=ban_time
            )
            await bot.send_message(chat_id=message.chat.id,
                                   text=f"Пользователь "
                                        f"\nбыл забанен на {ban_time}")
            await Database().sql_delete_reported_banned_users(bad_user_id_by_firstname[0]['telegram_id'])
        await bot.send_message(chat_id=bad_user_id_by_firstname[0]['telegram_id'],
                               text='На вас была отправлена жалоба!',
                               reply_markup=await report_message_button()
                               )

    else:
        await bot.send_message(chat_id=message.chat.id,
                               text='Вы ввели неверный @username или firstname')
        await state.finish()

async def start_username_fsm(call: types.CallbackQuery):
    await call.message.reply('Вы можете уменьшить количество жалоб на 1,'
                             '\nесли угадаете firstname , кто пожаловался')
    await Username.username.set()
    await bot.delete_message(chat_id=call.message.chat.id,
                       message_id=call.message.message_id)

async def load_username(message: types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['username'] = message.text
        username_who_reported = re.sub("@", "", data['username'])
        existing = await Database().sql_select_username_who_reported(username_who_reported=username_who_reported)
        if existing:
            await Database().sql_update_report_count(username_who_reported=existing[0]['username_who_reported'],
                                               telegram_id_complained_user=existing[0]['telegram_id_complained'],
                                               telegram_id_bad_user=existing[0]['telegram_id_bad_user']
                                               )
            await message.reply('Вы угадали и вам уменьшается количество'
                                '\nжалоб на 1 единицу.😎')
            await state.finish()
        else:
            await state.finish()
            await message.reply('К сожалению, вы не угадали 😞😞')


async def pass_chance(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.message.chat.id,
                       message_id=call.message.message_id)
    await bot.send_message(chat_id=call.message.chat.id,
                           text='Вы пропустили шанс😞')






def register_report_handler(dp: Dispatcher):
    dp.register_message_handler(start_report_fsm, commands=['report'])
    dp.register_message_handler(report_to_user,content_types=['text'],state=ReportUser.report)
    dp.register_message_handler(load_reason,content_types=['text'],state=ReportUser.reason)
    dp.register_callback_query_handler(start_username_fsm,lambda call: call.data == 'chance')
    dp.register_message_handler(load_username,content_types=['text'],state=Username.username)
    dp.register_callback_query_handler(pass_chance,lambda call: call.data == 'pass_button')
