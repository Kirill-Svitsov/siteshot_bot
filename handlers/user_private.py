import time
from datetime import datetime
import re

from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile

from constants.constants import *
from filters.chat_types import ChatTypeFilter
from keyboard.inline import git, more
from keyboard.reply import start_keyboard
from utils.loger import logger
from utils.make_shot import make_shot

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
    logger.info(f'{message.from_user.username} - начал работу с ботом.')


@user_private_router.message(F.text.lower() == 'привет')
@user_private_router.message(Command('hello'))
async def hello_cmd(message: types.Message):
    """Хэндлер на обработку URL и возвращения скриншота"""
    await message.reply(f'<b>{message.from_user.first_name}</b>' + GREETING_ANSWER)
    await message.answer_animation(HASBIK_HELLO)
    logger.info(f'{message.from_user.username} - использовал команду hello.')


@user_private_router.message(F.text.lower() == 'пока')
@user_private_router.message(Command('bye'))
async def bye_cmd(message: types.Message):
    """Хэндлер на обработку URL и возвращения скриншота"""
    await message.reply(BYE_ANSWER + f'<b>{message.from_user.first_name}</b>!')
    await message.answer_animation(BYE_STICKER)
    logger.info(f'{message.from_user.username} - использовал команду bye.')


@user_private_router.message(F.text.lower() == 'помощь')
@user_private_router.message(Command('help'))
async def help_cmd(message: types.Message):
    """Хэндлер на обработку URL и возвращения скриншота"""
    await message.answer(
        f'<b>{message.from_user.first_name}</b> ' + COMMAND_LIST,
        reply_markup=git
    )
    logger.info(f'{message.from_user.username} - использовал команду help.')


# Код для состояний машины FSM
class MakeShot(StatesGroup):
    url = State()
    process = State()
    screenshot_path = State()
    info = State()


# Хэндлер для запуска команды make_shot
@user_private_router.message(StateFilter(None), F.text.lower() == 'сделать скриншот')
@user_private_router.message(Command('make_shot'))
async def shot_cmd(message: types.Message, state: FSMContext):
    """Хэндлер для запуска команды make_shot"""
    await message.answer(
        f'<b>{message.from_user.first_name}</b> ' + URL_ANSWER,
        reply_markup=None
    )
    await state.set_state(MakeShot.url)
    logger.info(f'{message.from_user.username}  - использовал команду сделать скриншот.')


# Хэндлер получения скриншота
@user_private_router.message(MakeShot.url, F.text)
async def process_cmd(message: types.Message, state: FSMContext):
    """Хэндлер получения скриншота"""
    date = str(datetime.now())
    user_id = int(message.from_user.id)
    url = message.text
    start_time = time.time()
    url_pattern = re.compile(r'^https?://(?:[\w-]+\.?)+[\w]+(?:/\S*)?')
    if not url_pattern.match(url):
        await message.answer(
            "URL не соответствует шаблону. Пожалуйста, введите корректный URL."
        )
        logger.error(
            f'{message.from_user.username}'
            f' - использовал неккоретный URL: {message.text}'
        )
        return
    await state.update_data(url=message.text)
    process_message = await message.answer(
        'Получаю скриншот...\n'
        'К сожалению на это время другие комманды не работают 😪',
    )
    logger.info('Запущен процесс получения скриншота.')
    process_sticker = await message.answer_animation(PROCESS_STICKER)
    await state.set_state(MakeShot.process)

    # Хотел добавить таймер на долгий ответ, но selenium синхронная
    # Поэтому она выполниться в любом случае, и таймер не сработает.
    # async def timeout_handler():
    #     await asyncio.sleep(45)
    #     await message.answer("Извините, что-то пошло не так. Процесс занимает слишком много времени.")
    #     await state.set_state(MakeShot.url)
    #
    # # Запускаем таймер
    # timeout_task = asyncio.create_task(timeout_handler())

    result = await make_shot(date, user_id, url)
    if result:
        logger.info('Скриншот получен. Функция продолжает работу.')
        if len(result) == 3:
            logger.info('Функция вернула все аргуенты, в том числе и WHOIS.')
            screenshot_path, title, info = result
            await state.update_data(screenshot_path=screenshot_path)
            await state.update_data(info=info)
            await state.set_state(MakeShot.screenshot_path)
            # Сразу после установки состояния MakeShot.screenshot_path отправляем скриншот
            await send_screenshot(message, state, start_time, title, process_message, process_sticker, info)
        else:
            logger.info('Функция вернула скриншот, без WHOIS.')
            screenshot_path, title = result
            await state.update_data(screenshot_path=screenshot_path)
            await state.set_state(MakeShot.screenshot_path)
            # Сразу после установки состояния MakeShot.screenshot_path отправляем скриншот
            await send_screenshot(message, state, start_time, title, process_message, process_sticker)

    else:
        logger.error('Функция не вернула скриншот.')
        await message.answer(
            "Ошибка при создании скриншота, бот не может получить доступ к URL."
        )
        await state.clear()  # Отменяем состояние при ошибке


@user_private_router.message(MakeShot.screenshot_path)
async def send_screenshot(
        message: types.Message,
        state: FSMContext,
        start_time: float,
        title: str,
        process_message: types.Message,
        process_animation: types.Message,
        info: dict = None
):
    """Хэндлер отправки скриншота"""
    data = await state.get_data()  # Получаем данные из состояния
    screenshot_path = data.get('screenshot_path')  # Получаем путь к скриншоту из данных состояния
    url = data.get('url')  # Получаем URL из данных состояния
    finish_time = round((time.time() - start_time), 1)
    new_message_text = (
        f'✔ Скриншот сохранен и отправлен в чат:\n'
        f'🕸 Страница: <b>{title}</b>\n'
        f'🔗 URL: {url}\n'  # Используем URL из данных состояния
        f'⏱ Время обработки: <b>{finish_time} секунд(ы)</b>\n'
    )
    if info:
        logger.info('WHOIS отправлен в чат.')
        new_message_text += "Вот “Подробнее”, которая показывает WHOIS сайта"
        new_reply_markup = more
    else:
        logger.warning('WHOIS не отправлен в чат.')
        new_message_text += "К сожалению не удалось получить WHOIS сайта"
        new_reply_markup = None
        await state.clear()  # Завершаем состояние после отправки скриншота
    # Удаляем сообщение о процессе и
    await message.answer_photo(
        photo=FSInputFile(
            screenshot_path, filename=screenshot_path
        ), caption=new_message_text,
        reply_markup=new_reply_markup
    )
    logger.info('Скриншот отправлен в чат.')
    # Это скорее костыль, но изменить сообщение не удалось
    # Поэтому удаляю
    await process_message.delete()
    await process_animation.delete()
    # Отправляем стикер о завершении
    await message.answer_animation(DONE_STICKER)
    logger.info('Функция отправки скриншота завершила работу.')


@user_private_router.callback_query(F.data.in_(['подробнее', 'more']))
async def more_info_callback(query: types.CallbackQuery, state: FSMContext):
    # Обработка нажатия кнопки "Подробнее"
    await query.answer()
    # Получаем информацию из состояния или из базы данных
    data = await state.get_data()
    info = data.get('info')
    if info:
        logger.info('Нажата кнопка "Подробнее" к скриншоту.')
        # Отправляем информацию в чат
        await query.message.answer(f'Информация WHOIS:\n{info}')
    else:
        await query.message.answer('К сожалению информацию WHOIS добыть не удалось')
    await state.clear()
    logger.info(f'Состояние FSM машины сброшено.')
    # Удаление сообщения с кнопкой "Подробнее"
    await query.message.edit_reply_markup(reply_markup=None)


@user_private_router.message()
async def stub(message: types.Message):
    """Ответ - заглушка на неизвестные команды."""
    user = message.from_user.first_name
    if message.text:
        logger.info(f'{message.from_user.username} - ввел несуществующую команду.')
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
        logger.warning(f'{message.from_user.username} - отправил не текстовое сообщение.')
        await message.answer(NON_TYPE_ANSWER)
        await message.answer_animation(NON_TYPE_STICKER)
