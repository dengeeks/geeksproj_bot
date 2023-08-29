import binascii
import os

from aiogram import types
from aiogram.utils.deep_linking import _create_link

from config import bot
from database.sql_commands import Database
from keyboards.start_keyboard import send_money_to_user_button


async def create_reference_link(call: types.CallbackQuery):
    existed = await Database().sql_select_existed_link(
        telegram_id=call.from_user.id
    )
    if existed[0]['link'] is None:
        token = binascii.hexlify(os.urandom(4)).decode()
        link = await _create_link(link_type='start',payload=token)
        await Database().sql_update_telegram_user_link(reference_link=link,
                                                 telegram_id=call.from_user.id)
        await bot.send_message(
            chat_id=call.from_user.id,
            text=f"Ваша реферальная ссылка `{link}`\n"
                 f"кликните по ней чтобы сохранить ‼️",
            parse_mode=types.ParseMode.MARKDOWN
        )
    else:
        await bot.send_message(
            chat_id=call.from_user.id,
            text=f"Ваша реферальная ссылка `{existed[0]['link']}`\n"
                 f"кликните по ней чтобы сохранить ‼️",
            parse_mode=types.ParseMode.MARKDOWN
        )

async def reference_list_menu(call: types.CallbackQuery):
    referrals = await Database().sql_select_reference_users_by_owner_tg_id(
        owner_tg_id=call.from_user.id
    )
    referral_list = ['Список ваших рефералов🔗\n']
    if referrals:
        for referral in referrals:
            referral_list.append(f'[Реферал](tg://user?id={referral["referral_telegram_id"]})')
        referral_list = '\n'.join(referral_list)
        await bot.send_message(chat_id=call.from_user.id,
                               text=referral_list,
                               parse_mode=types.ParseMode.MARKDOWN)

async def my_balance_menu(call: types.CallbackQuery):
    balance = await Database().sql_select_my_balance(
        telegram_id=call.from_user.id
    )
    await bot.send_message(chat_id=call.from_user.id,
                           text=f'Ваш баланс равен - *{balance[0]["balance"]}*',
                           reply_markup= await send_money_to_user_button(),
                           parse_mode=types.ParseMode.MARKDOWN)



