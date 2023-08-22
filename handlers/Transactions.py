import re

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from config import bot
from database.sql_commands import Database
from aiogram.dispatcher.filters.state import State, StatesGroup


class SendMoney(StatesGroup):
    name_user = State()
    amount = State()


async def start_fsm_send_money(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Напишите @username или firstname пользователя\n'
                                'которому вы хотите отправить деньги💸')
    await SendMoney.name_user.set()


async def load_name(message: types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['name_user'] = re.sub("@","",message.text)
        user_telegram_id = Database().sql_select_users_balance_by_user_firsname(
            username=data['name_user'],
            firstname=data['name_user']
        )
    if user_telegram_id:
        await bot.send_message(chat_id=message.from_user.id,
                         text='Введите сколько хотите отправить? 🙌')
        await SendMoney.amount.set()
    else:
        await bot.send_message(chat_id=message.from_user.id,
                         text=f'Нет,такого пользователя *{data["name_user"]}*\n'
                         f'либо у него нет рефералов ❗❗❗',
                         parse_mode=types.ParseMode.MARKDOWN)

async def load_amount(message: types.Message,state: FSMContext):
    balance = Database().sql_select_my_balance(
        telegram_id=message.from_user.id
    )
    if int(message.text) <= balance[0]['balance']:
        async with state.proxy() as data:
            user_telegram_id = Database().sql_select_users_balance_by_user_firsname(
                username=data['name_user'],
                firstname=data['name_user']
            )
            data['amount'] = int(message.text)
        Database().sql_update_sender_balance(balance=data['amount'],
                                             telegram_id=message.from_user.id)
        Database().sql_update_balance_recipient_balance(balance=data['amount'],
                                                        telegram_id=user_telegram_id[0]["telegram_id"])
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'Пользователю *{data["name_user"]}* было отправлено *{data["amount"]}*',
                               parse_mode=types.ParseMode.MARKDOWN)
        Database().sql_select_into_transactions(
            Sender_id=message.from_user.id,
            Recipient_id=user_telegram_id[0]["telegram_id"],
            Amount=data['amount']
        )
        await state.finish()
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="У вас недостаточно средств 💰💰")



