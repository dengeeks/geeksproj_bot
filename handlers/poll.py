from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from database.sql_commands import Database
from config import PollState, bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



async def fsm_poll_start(message: types.Message):
    await message.reply('Какие новые идеи вы можете'
                        '\nпредложить для улучшения бота?')
    await PollState.idea.set()


async def load_idea(message: types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['idea'] = message.text
    await PollState.next()
    await message.reply('С какими проблемами вы встретились?')

async def load_problems(message: types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['problems'] = message.text
        Database().sql_insert_poll_answers(idea=data['idea'],
                                           problems=data['problems'],
                                           telegram_id=message.from_user.id)
    await message.reply('Ваш ответ принят!')
    await state.finish()


def register_poll_handlers(dp: Dispatcher):
    dp.register_message_handler(fsm_poll_start,commands=['poll'])
    dp.register_message_handler(load_idea,content_types=['text'],state=PollState.idea)
    dp.register_message_handler(load_problems,content_types=['text'],state=PollState.problems)