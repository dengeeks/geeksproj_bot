from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from database.sql_commands import Database
from config import PollState



async def fsm_poll_start(message: types.Message):
    telegram = await Database().sql_select_admin_list()
    result = tuple(d['admin_tg_id'] for d in telegram)
    if message.from_user.id in result:
        await message.reply('Админ не может пройти опрос!')
    else:
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
        await Database().sql_insert_poll_answers(idea=data['idea'],
                                           problems=data['problems'],
                                           telegram_id=message.from_user.id)
    await message.reply('Ваш ответ принят!')
    await state.finish()


def register_poll_handlers(dp: Dispatcher):
    dp.register_message_handler(fsm_poll_start,commands=['poll'])
    dp.register_message_handler(load_idea,content_types=['text'],state=PollState.idea)
    dp.register_message_handler(load_problems,content_types=['text'],state=PollState.problems)