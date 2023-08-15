from decouple import config
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup,State


storage = MemoryStorage()
TOKEN = config('TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot,storage=storage)

class UserState(StatesGroup):
    name = State()
    age = State()
    bio = State()
    photo = State()

class PollState(StatesGroup):
    idea = State()
    problems = State()

class AdminPollId(StatesGroup):
    id = State()