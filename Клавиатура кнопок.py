# Задача "Меньше текста, больше кликов":
# Необходимо дополнить код предыдущей задачи, чтобы вопросы о параметрах тела для расчёта калорий выдавались по нажатию кнопки.
# Измените massage_handler для функции set_age. Теперь этот хэндлер будет реагировать на текст 'Рассчитать', а не на 'Calories'.
# Создайте клавиатуру ReplyKeyboardMarkup и 2 кнопки KeyboardButton на ней со следующим текстом: 'Рассчитать' и 'Информация'.
# Сделайте так, чтобы клавиатура подстраивалась под размеры интерфейса устройства при помощи параметра resize_keyboard.
# Используйте ранее созданную клавиатуру в ответе функции start, используя параметр reply_markup.
# В итоге при команде /start у вас должна присылаться клавиатура с двумя кнопками.
#
# При нажатии на кнопку с надписью 'Рассчитать' срабатывает функция set_age с которой начинается работа машины состояний для age, growth и weight.


from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot_key import API

bot = Bot(token=API)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button1 = KeyboardButton('Рассчитать каллории')
button2 = KeyboardButton('Информация о боте')
kb.row(button1, button2)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start_calories(message):
    await message.answer('Что тебя интересует?', reply_markup=kb)


@dp.message_handler(text='Рассчитать каллории')
async def set_age(message):
    await message.answer('Введите свой возраст:')
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
