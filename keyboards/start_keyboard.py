from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def friend_unfriend_button(id):
    markup = InlineKeyboardMarkup()
    friend_button = InlineKeyboardButton('Друг👍🏻',
                                         callback_data=f'friend_button_{id}')
    unfriend_button = InlineKeyboardButton('Недруг👎🏻',
                                           callback_data='unfriend_button')
    markup.row(friend_button, unfriend_button)
    return markup


async def start_menu_button():
    markup = InlineKeyboardMarkup(row_width=2)
    play_game = InlineKeyboardButton('Друг👍🏻-Недруг?👎🏻',
                                     callback_data='play_game')
    create_link = InlineKeyboardButton('Реф. ссылка🔗',
                                       callback_data='reference_link')
    list_referral = InlineKeyboardButton('Список Рефералов📃',
                                         callback_data='list_referral')
    my_balance_button = InlineKeyboardButton('Мой баланс💵',
                                             callback_data='my_balance')
    markup.add(play_game, create_link, list_referral, my_balance_button)
    return markup



async def send_money_to_user_button():
    markup = InlineKeyboardMarkup()
    send_money = InlineKeyboardButton('Отправить деньги пользователю💸💸💸',
                                         callback_data='money')
    markup.row(send_money)
    return markup

