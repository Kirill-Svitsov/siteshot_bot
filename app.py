import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommandScopeAllPrivateChats
from dotenv import load_dotenv, find_dotenv

from common.bot_cmnds_list import private
from constants.constants import *
from handlers.user_private import user_private_router
from handlers.user_group import user_group_router

load_dotenv(find_dotenv())

bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
# Создаем диспетчер
dp = Dispatcher()
# dp.update.middleware(DataBaseSession(session_pool=session_maker))
# Подключаем роутеры к диспетчеру
dp.include_routers(user_private_router, user_group_router)


async def main():
    """Ассинхронная функция запуска бота"""
    # Пропускаем обновления, которые были до включения бота
    await bot.delete_webhook(drop_pending_updates=True)
    # Создаем меню/команды бота
    await bot.set_my_commands(commands=private, scope=BotCommandScopeAllPrivateChats())
    # Запускаем polling
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


# Запуск бота
asyncio.run(main())
