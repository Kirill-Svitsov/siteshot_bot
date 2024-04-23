from datetime import datetime
import re

from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile

from constants.constants import *
from filters.chat_types import ChatTypeFilter
from keyboard.reply import start_keyboard
from handlers.make_shot import make_shot

user_private_router = Router()
# Устанавливаем фильтрацию на роутер для хэндлеров приватных чатов
user_private_router.message.filter(ChatTypeFilter(["private"]))


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    """Start command для бота."""
    await message.answer(
        f'<b>{message.from_user.first_name}</b>' + GREETING_ANSWER,
        reply_markup=start_keyboard
    )
    await message.answer_animation(HASBIK_HELLO)


@user_private_router.message(F.text.lower() == 'привет')
@user_private_router.message(Command('hello'))
async def hello_cmd(message: types.Message):
    """Хэндлер на обработку URL и возвращения скриншота"""
    await message.reply(f'<b>{message.from_user.first_name}</b>' + GREETING_ANSWER)
    await message.answer_animation(HASBIK_HELLO)


@user_private_router.message(F.text.lower() == 'пока')
@user_private_router.message(Command('bye'))
async def bye_cmd(message: types.Message):
    """Хэндлер на обработку URL и возвращения скриншота"""
    await message.reply(BYE_ANSWER + f'<b>{message.from_user.first_name}</b>!')
    await message.answer_animation(BYE_STICKER)


@user_private_router.message(F.text.lower() == 'помощь')
@user_private_router.message(Command('help'))
async def help_cmd(message: types.Message):
    """Хэндлер на обработку URL и возвращения скриншота"""
    await message.answer(f'<b>{message.from_user.first_name}</b> ' + COMMAND_LIST)


# Код для состояний машины FSM
class MakeShot(StatesGroup):
    url = State()
    process = State()
    screenshot_path = State()


# Хэндлер для запуска команды make_shot
@user_private_router.message(StateFilter(None), F.text.lower() == 'сделать скриншот')
@user_private_router.message(Command('make_shot'))
async def shot_cmd(message: types.Message, state: FSMContext):
    """Хэндлер для запуска команды make_shot"""
    await message.answer(
        f'<b>{message.from_user.first_name}</b> ' + URL_ANSWER,
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(MakeShot.url)


# Хэндлер на отмену команды make_shot
@user_private_router.message(F.text.lower() == 'отмена')
@user_private_router.message(Command('/cancel'))
async def cancel_cmd(message: types.Message, state: FSMContext):
    """Хэндлер на отмену команды make_shot"""
    await message.answer(
        f'Действия отменены',
        reply_markup=start_keyboard
    )
    await state.finish()  # Отменяем состояние при отмене команды


# Хэндлер получения скриншота
@user_private_router.message(MakeShot.url, F.text)
async def process_cmd(message: types.Message, state: FSMContext):
    """Хэндлер получения скриншота"""
    date = str(datetime.now())
    user_id = int(message.from_user.id)
    url = message.text
    if not re.match(r'https?://(?:www\.)?example\.com', url):
        await message.answer("URL не соответствует шаблону. Пожалуйста, введите корректный URL.")
        return
    await state.update_data(url=message.text)
    await message.answer(
        f'Получаю скриншот по адресу: {message.text}',
    )
    await message.answer_animation(PROCESS_STICKER)
    await state.set_state(MakeShot.process)
    screenshot_path = await make_shot(date, user_id, url)
    if screenshot_path:
        await state.update_data(screenshot_path=screenshot_path)
        await state.set_state(MakeShot.screenshot_path)
        # Сразу после установки состояния MakeShot.screenshot_path отправляем скриншот
        await send_screenshot(message, state)
    else:
        await message.answer("Ошибка при создании скриншота.")
        await state.clear()  # Отменяем состояние при ошибке


# Хэндлер отправки скриншота
@user_private_router.message(MakeShot.screenshot_path)
async def send_screenshot(message: types.Message, state: FSMContext):
    """Хэндлер отправки скриншота"""
    data = await state.get_data()
    screenshot_path = data.get('screenshot_path')
    await message.answer_photo(
        photo=FSInputFile(
            screenshot_path, filename=screenshot_path
        ), caption=f'Скриншот сохранен и отправлен в чат:\n'
                   f'Это заняло вот столько времени = \n'
                   f'Вот “Подробнее”, которая показывает WHOIS сайта',
        reply_markup=start_keyboard
    )
    await message.answer_animation(DONE_STICKER)
    await state.clear()  # Завершаем состояние после отправки скриншота


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
