from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from database.sql_commands import Database
from config import UserState, bot
from aiogram.types import ContentType
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def fms_signup_start(message: types.Message):
    await message.reply('Укажите ваше имя - ')
    await UserState.name.set()


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await UserState.next()
    await message.reply('Укажите ваш возраст - ')


async def load_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if isinstance(int(message.text), int):
            data['age'] = message.text
            await UserState.next()
            await message.reply('Напишите о себе - ')
        else:
            await message.reply('Укажите ваш возраст в цифрах !')
            await state.finish()


async def load_bio(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['bio'] = message.text
    await UserState.next()
    await message.reply('Отправьте ваше фото - ')


async def load_photo(message: types.Message, state: FSMContext):
    path = await message.photo[-1].download(
        destination_dir='C:/Users/denis/PycharmProjects/hw1_month3/media')
    print(f'message.photo: {path.name}')
    async with state.proxy() as data:
        data['photo'] = message.photo
        Database().sql_insert_user_info(telegram_id=message.from_user.id,
                                        name_of_user=data['name'],
                                        age=data['age'],
                                        bio=data['bio'],
                                        photo=path.name)
        await message.reply('Вы зарегистрированны!', reply_markup=await profile_button())

    await state.finish()


async def profile_button():
    markup = InlineKeyboardMarkup()
    profile_button = InlineKeyboardButton('Мой профиль',
                                          callback_data='profile')
    markup.add(profile_button)
    return markup


async def get_profile(call: types.CallbackQuery):
    user_info = Database().sql_select_user_info(telegram_id=call.from_user.id)
    with open(user_info[0]['photo'], 'rb') as photo:
        await bot.send_photo(chat_id=call.message.chat.id,
                             photo=photo,
                             caption=f"Имя: {user_info[0]['name']}"
                                     f"\nВозраст: {user_info[0]['age']}"
                                     f"\nБиография: {user_info[0]['bio']}")


def register_signup_handlers(dp: Dispatcher):
    dp.register_message_handler(fms_signup_start, commands=['signup'])
    dp.register_message_handler(load_name, content_types=['text'], state=UserState.name)
    dp.register_message_handler(load_age, content_types=['text'], state=UserState.age)
    dp.register_message_handler(load_bio, content_types=['text'], state=UserState.bio)
    dp.register_message_handler(load_photo, content_types=ContentType.PHOTO, state=UserState.photo)
    dp.register_callback_query_handler(get_profile,lambda call:call.data == 'profile')
