import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

ALLOWED_UPDATES = ['message', 'edited_message', 'callback_query']

bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

GREETINGS_WORDS = (
    'привет',
    'здравствуй',
    'хай',
    'хэллоу',
    'hi',
    'hello'
)
FAREWELL_WORDS = (
    'пока',
    'пакеда',
    'до свидания',
    'всего хорошего',
    'бай',
    'bye'
)


@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    """Start command для бота."""
    await message.answer('Привет!')


@dp.message()
async def stub(message: types.Message):
    """Ответ - заглушка на неизвестные команды."""
    user = message.from_user.first_name
    if message.text:
        text = message.text
        if text.lower() in GREETINGS_WORDS:
            await message.answer(f'Дорогой <b>{user}</b> - здравствуй!\n'
                                 f'Чтобы узнать какие команды у меня есть, нажми /help')
        elif text.lower() in FAREWELL_WORDS:
            await message.answer(f'До свиданий, дорогой <b>{user}</b>!')
        else:
            await message.answer(f'Дорогой <b>{user}</b>, '
                                 f'к сожалению у меня нет команды: <b>{text}</b>\n'
                                 f'Вот список моих комманд: ')
    else:
        await message.answer(f'Дорогой <b>{user}</b>, '
                             f'к сожалению на текущий момент я умею работать только с текстом'
                             f'Вот список моих комманд: ')


async def main():
    """Ассинхронная функция запуска бота"""
    await dp.start_polling(bot)


# Запуск бота
asyncio.run(main())
