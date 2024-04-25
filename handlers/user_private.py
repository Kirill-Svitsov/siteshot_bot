from datetime import datetime
import re
import time

from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile

from constants import constants
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
        f'<b>{message.from_user.first_name}</b> '
        f'{constants.GREETING_ANSWER}',
        reply_markup=start_keyboard
    )
    await message.answer_animation(constants.HASBIK_HELLO)
    logger.info(f'{message.from_user.username} - '
                f'начал работу с ботом.')


@user_private_router.message(F.text.lower() == 'привет')
@user_private_router.message(Command('hello'))
async def hello_cmd(message: types.Message):
    """Хэндлер на обработку /hello и сообщения 'привет'"""
    await message.reply(f'<b>{message.from_user.first_name}</b> '
                        f'{constants.GREETING_ANSWER}')
    await message.answer_animation(constants.HASBIK_HELLO)
    logger.info(f'{message.from_user.username} - '
                f'использовал команду hello.')


@user_private_router.message(F.text.lower() == 'пока')
@user_private_router.message(Command('bye'))
async def bye_cmd(message: types.Message):
    """Хэндлер на обработку /bye и сообщения 'пока'"""
    await message.reply(
        f'{constants.BYE_ANSWER} '
        f'<b>{message.from_user.first_name}</b>!'
    )
    await message.answer_animation(constants.BYE_STICKER)
    logger.info(f'{message.from_user.username} - '
                f'использовал команду bye.')


@user_private_router.message(F.text.lower() == 'помощь')
@user_private_router.message(Command('help'))
async def help_cmd(message: types.Message):
    """Хэндлер на обработку /help и сообщения 'помощь'"""
    await message.answer(
        f'<b>{message.from_user.first_name}</b> '
        f'{constants.COMMAND_LIST}',
        reply_markup=git
    )
    logger.info(f'{message.from_user.username} -'
                f' использовал команду help.')


# Код для состояний машины FSM
class MakeShot(StatesGroup):
    url = State()
    process = State()
    screenshot_path = State()
    info = State()


@user_private_router.message(
    StateFilter(None),
    F.text.lower() == 'сделать скриншот'
)
@user_private_router.message(Command('make_shot'))
async def shot_cmd(message: types.Message, state: FSMContext):
    """Хэндлер для запуска команды make_shot"""
    await message.answer(
        f'<b>{message.from_user.first_name}</b> ' + constants.URL_ANSWER,
    )
    await state.set_state(MakeShot.url)
    logger.info(f'{message.from_user.username}'
                f'  - использовал команду сделать скриншот.')


@user_private_router.message(MakeShot.url, F.text)
async def process_cmd(message: types.Message, state: FSMContext):
    """Хэндлер получения скриншота"""
    date = str(datetime.now())
    user_id = int(message.from_user.id)
    url = message.text
    # Создаем стартовую метку времени
    start_time = time.time()
    # Создаем маску на проверку URL
    url_pattern = re.compile(r'^https?://(?:[\w-]+\.?)+[\w]+(?:/\S*)?')
    if not url_pattern.match(url):
        await message.answer(
            "URL не соответствует шаблону."
            " Пожалуйста, введите корректный URL."
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
    process_sticker = await message.answer_animation(
        constants.PROCESS_STICKER
    )
    await state.set_state(MakeShot.process)
    result = await make_shot(date, user_id, url)
    if result:
        logger.info('Скриншот получен. Функция продолжает работу.')
        if len(result) == 3:
            logger.info('Функция вернула все аргуенты,'
                        ' в том числе и WHOIS.')
            screenshot_path, title, info = result
            await state.update_data(screenshot_path=screenshot_path)
            await state.update_data(info=info)
            await state.set_state(MakeShot.screenshot_path)
            await send_screenshot(
                message, state, start_time,
                title, process_message,
                process_sticker, info
            )
        elif len(result) == 2:
            logger.info('Функция вернула скриншот, без WHOIS.')
            screenshot_path, title = result
            await state.update_data(screenshot_path=screenshot_path)
            await state.set_state(MakeShot.screenshot_path)
            await send_screenshot(
                message, state, start_time,
                title, process_message,
                process_sticker
            )
        else:
            logger.error(
                'Функция make_shot вернула'
                ' неожиданное количество аргументов'
            )
            await message.answer(constants.EXCEPTION_ANSWER)

    else:
        logger.error('Функция не вернула скриншот.')
        await message.answer(
            "Ошибка при создании скриншота,"
            " бот не может получить доступ к URL."
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
    # Получаем данные из состояния
    data = await state.get_data()
    # Получаем путь к скриншоту из данных состояния
    screenshot_path = data.get('screenshot_path')
    # Получаем URL из данных состояния
    url = data.get('url')
    # Фиксируем время выполнения функции
    finish_time = round((time.time() - start_time), 1)
    new_message_text = (
        f'✔ Скриншот сохранен и отправлен в чат:\n'
        f'🕸 Страница: <b>{title}</b>\n'
        f'🔗 URL: {url}\n'
        f'⏱ Время обработки: <b>{finish_time} секунд(ы)</b>\n'
    )
    if info:
        logger.info('WHOIS отправлен в чат.')
        new_message_text += ("Вот “Подробнее”,"
                             " которая показывает WHOIS сайта")
        new_reply_markup = more
    else:
        logger.warning('WHOIS не будет отправлен в чат.')
        new_message_text += ("К сожалению не удалось"
                             " получить WHOIS сайта")
        new_reply_markup = None
        # Завершаем состояние после отправки скриншота
        await state.clear()
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
    await message.answer_animation(constants.DONE_STICKER)
    logger.info(
        'Функция отправки скриншота завершила работу.'
    )


@user_private_router.callback_query(
    F.data.in_(['подробнее', 'more'])
)
async def more_info_callback(
        query: types.CallbackQuery,
        state: FSMContext
):
    """Фунция обработки callback 'Подробнее', при наличии WHOIS"""
    await query.answer()
    # Получаем информацию из состояния или из базы данных
    data = await state.get_data()
    info = data.get('info')
    if info:
        # Проверка - страховка
        logger.info('Нажата кнопка "Подробнее" к скриншоту.')
        # Отправляем информацию в чат
        await query.message.answer(
            f'Информация WHOIS:\n{info}'
        )
    else:
        await query.message.answer(
            'К сожалению информацию WHOIS добыть не удалось'
        )
    # Сбрасываем состояние машины
    await state.clear()
    logger.info('Состояние FSM машины сброшено.')
    # Удаление сообщения с кнопкой "Подробнее"
    await query.message.edit_reply_markup(reply_markup=None)


@user_private_router.message()
async def stub(message: types.Message):
    """Ответ - заглушка на неизвестные команды."""
    if message.text:
        logger.info(
            f'{message.from_user.username}'
            f' - ввел несуществующую команду.'
        )
        text = message.text
        if text.lower() in constants.GREETINGS_WORDS:
            await hello_cmd(message)
        elif text.lower() in constants.FAREWELL_WORDS:
            await bye_cmd(message)
        else:
            await message.answer(
                f'{constants.UNKNOWN_ANSWER}'
                f' <b>{text}</b>\n '
                f'{constants.COMMAND_LIST}'
            )
            await message.answer_animation(constants.UNKNOWN_STICKER)
    else:
        logger.warning(
            f'{message.from_user.username} - '
            f'отправил не текстовое сообщение.'
        )
        await message.answer(constants.NON_TYPE_ANSWER)
        await message.answer_animation(constants.NON_TYPE_STICKER)
