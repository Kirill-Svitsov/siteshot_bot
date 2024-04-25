import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommandScopeAllPrivateChats
from dotenv import load_dotenv, find_dotenv

from common.bot_cmnds_list import private
from constants import constants
from handlers.user_private import user_private_router
from handlers.user_group import user_group_router
from utils.loger import logger

load_dotenv(find_dotenv())

bot = Bot(
    token=os.getenv('TOKEN'),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()
dp.include_routers(user_private_router, user_group_router)


async def on_startup(bot):
    logger.info('Бот запущен')


async def on_shutdown(bot):
    logger.info('Бот выключен')


async def main():
    """Ассинхронная функция запуска бота"""
    try:
        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.set_my_commands(
            commands=private,
            scope=BotCommandScopeAllPrivateChats()
        )
        await dp.start_polling(
            bot,
            allowed_updates=constants.ALLOWED_UPDATES
        )
    except Exception as e:
        logger.critical(f"Произошла ошибка при запуске бота: {e}")


asyncio.run(main())
