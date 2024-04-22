from aiogram import types, Router
from aiogram.filters import CommandStart, Command

from constants.constants import *

user_private_router = Router()


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    """Start command для бота."""
    await message.answer(f'<b>{message.from_user.first_name}</b>' + GREETING_ANSWER)
    await message.answer_animation(HASBIK_HELLO)


@user_private_router.message(Command('hello'))
async def hello_cmd(message: types.Message):
    """Хэндлер на обработку URL и возвращения скриншота"""
    await message.reply(f'<b>{message.from_user.first_name}</b>' + GREETING_ANSWER)
    await message.answer_animation(HASBIK_HELLO)


@user_private_router.message(Command('bye'))
async def bye_cmd(message: types.Message):
    """Хэндлер на обработку URL и возвращения скриншота"""
    await message.reply(BYE_ANSWER + f'<b>{message.from_user.first_name}</b>!')
    await message.answer_animation(BYE_STICKER)


@user_private_router.message(Command('help'))
async def help_cmd(message: types.Message):
    """Хэндлер на обработку URL и возвращения скриншота"""
    await message.answer(f'<b>{message.from_user.first_name}</b> ' + COMMAND_LIST)


@user_private_router.message(Command('make_shot'))
async def shot_cmd(message: types.Message):
    """Хэндлер на обработку URL и возвращения скриншота"""
    await message.answer(f'<b>{message.from_user.first_name}</b> ' + URL_ANSWER)
    print(message.text)


@user_private_router.message()
async def stub(message: types.Message):
    """Ответ - заглушка на неизвестные команды."""
    user = message.from_user.first_name
    if message.text:
        text = message.text
        if text.lower() in GREETINGS_WORDS:
            await message.reply(f'<b>{user}</b>' + GREETING_ANSWER)
            await message.answer_animation(HASBIK_HELLO)
        elif text.lower() in FAREWELL_WORDS:
            await message.reply(BYE_ANSWER + f'<b>{user}</b>!')
            await message.answer_animation(BYE_STICKER)
        else:
            await message.answer(
                UNKNOWN_ANSWER + f'<b>{text}</b>\n' + COMMAND_LIST
            )
            await message.answer_animation(UNKNOWN_STICKER)
    else:
        await message.answer(NON_TYPE_ANSWER)
        await message.answer_animation(NON_TYPE_STICKER)
