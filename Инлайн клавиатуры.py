from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot_key import API

bot = Bot(token=API)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = InlineKeyboardMarkup()
button1 = InlineKeyboardButton('Рассчитать норму калорий', callback_data='calories')
button2 = InlineKeyboardButton('Формулы расчёта', callback_data='formulas')
kb.row(button1, button2)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb)


@dp.callback_query_handler(text='formulas')
async def formulas(call):
    await call.message.answer('10 x вес(кг) + 6.25 x рост(см) - 5 x возраст(лет) - 161')
    await call.answer()


@dp.message_handler(commands=['start'])
async def start_calories(message):
    await message.answer('Выберите опцию:', reply_markup=kb)


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(text='Информация о боте')
async def info(message):
    await message.answer('Я бот, помогающий твоему здоровью!', reply_markup=kb)


@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение')


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    weight_ = data["weight"]
    growth_ = data["growth"]
    age_ = data["age"]
    calories = 10 * int(weight_) + int(6.25) * int(growth_) - 5 * int(age_) - 161
    await message.answer(f'Ваша норма калорий: {calories}', reply_markup=kb)
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
