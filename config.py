from decouple import config
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup,State

PROXY_URL = "http://proxy.server:3128"
storage = MemoryStorage()
TOKEN = config('TOKEN')
bot = Bot(token=TOKEN,proxy=PROXY_URL)
dp = Dispatcher(bot,storage=storage)

class UserState(StatesGroup):
    name = State()
    age = State()
    bio = State()
    photo = State()

class PollState(StatesGroup):
    idea = State()
    problems = State()

class AdminId(StatesGroup):
    id = State()
class AdminAnswer(StatesGroup):
    answer = State()
class AdminRating(StatesGroup):
    rating = State()



