from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from bot_key import API

bot = Bot(token=API)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply('Привет!😊 \nЯ бот, который поможёт тебе подобрать фильм для просмотра')
    await message.answer('Напиши свое имя', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler()
async def name(message: types.Message):
    await message.answer(f'Приятно познакомиться, {message.text}!\nВыбери свою любимую категорию')


@dp.message_handler()
async def all_messages(message: types.Message):
    await message.reply('Введите команду /start, чтобы начать общение')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
