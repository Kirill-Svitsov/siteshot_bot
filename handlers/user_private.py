import re
import time
from datetime import datetime

from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile, ReplyKeyboardRemove

from constants import constants
from database.orm_query import orm_add_screenshot, orm_add_log
from filters.chat_types import ChatTypeFilter
from keyboard.inline import git, more
from keyboard.reply import ru_keyboard, en_keyboard, choose_language, lng
from sqlalchemy.ext.asyncio import AsyncSession
from utils.loger import logger
from utils.make_shot import make_shot
from utils.ensure_user_exists import ensure_user_exists
from utils.logs_script import logs_script

from database.models import User

user_private_router = Router()
# Устанавливаем фильтрацию на роутер для хэндлеров приватных чатов
user_private_router.message.filter(ChatTypeFilter(["private"]))
# По умолчанию устанавливаем русский язык
CHOSEN_LANGUAGE = constants.RU


class LanguageState(StatesGroup):
    language = State()


@user_private_router.message(CommandStart())
async def command_start(message: types.Message, session: AsyncSession) -> None:
    await message.answer(
        f'<b>{message.from_user.first_name}</b> '
        f'{constants.START_ANSWER}',
        reply_markup=lng
    )
    # Проверка или добавление пользователя в БД, при выполнении команды
    user = await ensure_user_exists(session, message)
    log = f'{message.from_user.username} начал работу с ботом.'
    logger.info(log)
    log = f'INFO ({str(datetime.now())}): ' + log
    await logs_script(session, user.id, log)


@user_private_router.message(
    (F.text.lower() == 'chose language') | (F.text.lower() == 'выбрать язык')
)
@user_private_router.message(Command('choose_language'))
async def choose_language_cmd(message: types.Message, state: FSMContext, session: AsyncSession):
    """Хэндлер на обработку /hello и сообщения 'привет'"""
    # Проверка или добавление пользователя в БД, при выполнении команды
    await ensure_user_exists(session, message)
    await state.set_state(LanguageState.language)
    await message.answer('Выберите язык: ', reply_markup=choose_language)
    logger.info(f'{message.from_user.first_name} выбирает язык.')


@user_private_router.message(LanguageState.language)
async def set_language(message: types.Message, state: FSMContext, session: AsyncSession) -> None:
    global CHOSEN_LANGUAGE
    await state.update_data(language=message.text)
    language = message.text.lower()
    CHOSEN_LANGUAGE = language
    user = await ensure_user_exists(session, message)
    if language == 'русский':
        await state.update_data(language=message.text)
        await message.answer(
            'Отлично! Продолжим на русском языке.',
            reply_markup=ru_keyboard
        )
        log = f'{message.from_user.username} выбрал русский язык.'
        logger.info(log)
        log = f'INFO ({str(datetime.now())}): ' + log
        await logs_script(session, user.id, log)
        await state.clear()
    elif language == 'english':
        await message.answer(
            'Great! Lets continue in English.',
            reply_markup=en_keyboard
        )
        log = f'{message.from_user.username} выбрал английский язык.'
        logger.info(log)
        log = f'INFO ({str(datetime.now())}): ' + log
        await logs_script(session, user.id, log)
        await state.update_data(language=message.text)
        await state.clear()
    else:
        await message.answer(
            'Вероятно вы ввели что-то не то.'
            'Пожалуйста выберите язык снова:',
            reply_markup=choose_language
        )
        log = f'{message.from_user.username} ошибся при выборе языка.'
        logger.warning(log)
        log = f'WARNING ({str(datetime.now())}): ' + log
        await logs_script(session, user.id, log)


@user_private_router.message((F.text.lower() == 'привет') | (F.text.lower() == 'hello'))
@user_private_router.message(Command('hello'))
async def hello_cmd(message: types.Message, session: AsyncSession):
    global CHOSEN_LANGUAGE
    """Хэндлер на обработку /hello и сообщения 'привет'"""
    # Проверка или добавление пользователя в БД, при выполнении команды
    user = await ensure_user_exists(session, message)
    if CHOSEN_LANGUAGE == constants.RU:
        await message.reply(f'<b>{message.from_user.first_name}</b> '
                            f'{constants.GREETING_ANSWER_RU}')
    else:
        await message.reply(f'<b>{message.from_user.first_name}</b> '
                            f'{constants.GREETING_ANSWER_EN}')
    await message.answer_animation(constants.HASBIK_HELLO)
    log = f'{message.from_user.username} - использовал команду hello.'
    logger.info(log)
    log = f'INFO ({str(datetime.now())}): ' + log
    await logs_script(session, user.id, log)


@user_private_router.message((F.text.lower() == 'пока') | (F.text.lower() == 'bye'))
@user_private_router.message(Command('bye'))
async def bye_cmd(message: types.Message, session: AsyncSession):
    """Хэндлер на обработку /bye и сообщения 'пока'"""
    # Проверка или добавление пользователя в БД, при выполнении команды
    user = await ensure_user_exists(session, message)
    global CHOSEN_LANGUAGE
    if CHOSEN_LANGUAGE == constants.RU:
        await message.reply(
            f'{constants.BYE_ANSWER_RU} '
            f'<b>{message.from_user.first_name}</b>!'
        )
    else:
        await message.reply(
            f'{constants.BYE_ANSWER_EN} '
            f'<b>{message.from_user.first_name}</b>!'
        )
    await message.answer_animation(constants.BYE_STICKER)
    log = f'{message.from_user.username} - использовал команду bye.'
    logger.info(log)
    log = f'INFO ({str(datetime.now())}): ' + log
    await logs_script(session, user.id, log)


@user_private_router.message((F.text.lower() == 'помощь') | (F.text.lower() == 'help'))
@user_private_router.message(Command('help'))
async def help_cmd(message: types.Message, session: AsyncSession):
    """Хэндлер на обработку /help и сообщения 'помощь'"""
    # Проверка или добавление пользователя в БД, при выполнении команды
    user = await ensure_user_exists(session, message)
    global CHOSEN_LANGUAGE
    if CHOSEN_LANGUAGE == constants.RU:
        await message.answer(
            f'<b>{message.from_user.first_name}</b> \n'
            f'{constants.COMMAND_LIST_RU}',
            reply_markup=git
        )
    else:
        await message.answer(
            f'<b>{message.from_user.first_name}</b> \n'
            f'{constants.COMMAND_LIST_EN}',
            reply_markup=git
        )
    log = f'{message.from_user.username} - использовал команду help.'
    logger.info(log)
    log = f'INFO ({str(datetime.now())}): ' + log
    await logs_script(session, user.id, log)


# Код для состояний машины FSM для скриншота
class MakeShot(StatesGroup):
    user_id = State()
    screenshot_path = State()
    info = State()


@user_private_router.message(
    StateFilter(None),
    (F.text.lower() == 'сделать скриншот') | (F.text.lower() == 'make screen')
)
@user_private_router.message(Command('make_shot'))
async def shot_cmd(message: types.Message, state: FSMContext, session: AsyncSession):
    """Хэндлер для запуска команды make_shot"""
    # Создаем юзера, если его нет и получаем обратно, или просто получаем юзера
    user = await ensure_user_exists(session, message)
    global CHOSEN_LANGUAGE
    if CHOSEN_LANGUAGE == constants.RU:
        await message.answer(
            f'<b>{message.from_user.first_name}</b> ' + constants.URL_ANSWER_RU,
        )
    else:
        await message.answer(
            f'<b>{message.from_user.first_name}</b> ' + constants.URL_ANSWER_EN,
        )
    await state.set_state(MakeShot.user_id)
    await state.update_data(user_id=user.id)
    log = f'{message.from_user.username} - - использовал команду сделать скриншот.'
    logger.info(log)
    log = f'INFO ({str(datetime.now())}): ' + log
    await logs_script(session, user.id, log)


@user_private_router.message(MakeShot.user_id, F.text)
async def process_cmd(message: types.Message, state: FSMContext, session: AsyncSession):
    """Хэндлер получения скриншота"""
    global CHOSEN_LANGUAGE
    user = await ensure_user_exists(session, message)
    date = str(datetime.now())
    telegram_user_id = int(message.from_user.id)
    url = message.text
    # Создаем стартовую метку времени
    start_time = time.time()
    # Создаем маску на проверку URL
    url_pattern = re.compile(r'^https?://(?:[\w-]+\.?)+[\w]+(?:/\S*)?')
    # По хорошему нужно добавить обработку, когда URL высылают без протокола
    # то - есть www.vk.ru - условно
    if CHOSEN_LANGUAGE == constants.RU:
        wrong_url_answer_answer = constants.WRONG_URL_RU
        process_message = constants.PROCESS_MESSAGE_RU
        keyboard = ru_keyboard
    else:
        wrong_url_answer_answer = constants.WRONG_URL_EN
        process_message = constants.PROCESS_MESSAGE_EN
        keyboard = en_keyboard
    if not url_pattern.match(url):
        await message.answer(
            text=wrong_url_answer_answer,
            reply_markup=keyboard
        )
        log = (f'{message.from_user.username} - использовал '
               f'некорретный URL: {message.text}')
        logger.error(log)
        log = f'ERROR ({str(datetime.now())}): ' + log
        await logs_script(session, user.id, log)
        return
    process_message = await message.answer(
        text=process_message,
        reply_markup=keyboard
    )
    log = (f'Запущен процесс получения скриншота'
           f'по URL = {url}')
    logger.info(log)
    log = f'INFO ({str(datetime.now())}): ' + log
    await logs_script(session, user.id, log)
    process_sticker = await message.answer_animation(
        constants.PROCESS_STICKER
    )
    result = await make_shot(date, telegram_user_id, url)
    if result:
        logger.info('Скриншот получен. Функция продолжает работу.')
        if len(result) == 3:
            log = 'Функция вернула все аргуенты, в том числе и WHOIS.'
            logger.info(log)
            log = f'INFO ({str(datetime.now())}): ' + log
            await logs_script(session, user.id, log)
            screenshot_path, title, info = result
            await state.update_data(screenshot_path=screenshot_path)
            await state.update_data(info=info)
            await state.set_state(MakeShot.screenshot_path)
            await send_screenshot(
                user, message, state, start_time,
                title, process_message,
                process_sticker, session, info
            )
        elif len(result) == 2:
            log = 'Функция вернула скриншот, без WHOIS.'
            logger.info(log)
            log = f'INFO ({str(datetime.now())}): ' + log
            await logs_script(session, user.id, log)
            screenshot_path, title = result
            await state.update_data(screenshot_path=screenshot_path)
            await state.set_state(MakeShot.screenshot_path)
            await send_screenshot(
                user, message, state, start_time,
                title, process_message,
                process_sticker, session
            )
    else:
        log = 'Функция make_shot не получила доступ к сайту.'
        logger.error(log)
        log = f'ERROR ({str(datetime.now())}): ' + log
        await logs_script(session, user.id, log)
        await state.clear()
        logger.info('Состояние FSM машины сброшено.')
        await process_message.delete()
        await process_sticker.delete()
        await message.answer(constants.EXCEPTION_ANSWER)


@user_private_router.message(MakeShot.screenshot_path)
async def send_screenshot(
        user: User,
        message: types.Message,
        state: FSMContext,
        start_time: float,
        title: str,
        process_message: types.Message,
        process_animation: types.Message,
        session: AsyncSession,
        info: dict = None,
):
    """Хэндлер отправки скриншота"""
    global CHOSEN_LANGUAGE
    # Получаем данные из состояния
    data = await state.get_data()
    # Получаем путь к скриншоту из данных состояния
    screenshot_path = data.get('screenshot_path')
    # Получаем URL из данных состояния
    url = data.get('url')
    # Фиксируем время выполнения функции
    finish_time = round((time.time() - start_time), 1)
    if CHOSEN_LANGUAGE == constants.RU:
        new_message_text = (
            f'✔ Скриншот сохранен и отправлен в чат:\n'
            f'🕸 Страница: <b>{title}</b>\n'
            f'🔗 URL: {url}\n'
            f'⏱ Время обработки: <b>{finish_time} секунд(ы)</b>\n'
        )
        additional_text = ("Вот “Подробнее”,"
                           " которая показывает WHOIS сайта")
        without_whois_message = ("К сожалению, не удалось"
                                 " получить WHOIS сайта")
        keyboard = ru_keyboard
    else:
        new_message_text = (
            f'✔ Screenshot saved and sent to the chat:\n'
            f'🕸 Page: <b>{title}</b>\n'
            f'🔗 URL: {url}\n'
            f'⏱ Processing time: <b>{finish_time} seconds(s)</b>\n'
        )
        additional_text = ("Here is the 'More',"
                           " which shows the WHOIS of the site")
        without_whois_message = ("Unfortunately, it was not possible to"
                                 " get the WHOIS of the site")
        keyboard = en_keyboard
    if info:
        log = 'WHOIS отправлен в чат.'
        logger.info(log)
        log = f'INFO ({str(datetime.now())}): ' + log
        await logs_script(session, user.id, log)
        new_message_text += additional_text
        new_reply_markup = more
        # Добавляем скриншот в БД.
        try:
            await orm_add_screenshot(session, data)
            log = 'Скриншот добавлен в БД.'
            logger.info(log)
            log = f'INFO ({str(datetime.now())}): ' + log
            await logs_script(session, user.id, log)
        except Exception as e:
            log = f'Скриншот добавлен в БД. Причина: {e}.'
            logger.error(log)
            log = f'ERROR ({str(datetime.now())}): ' + log
            await logs_script(session, user.id, log)
    else:
        log = 'WHOIS не будет отправлен в чат.'
        logger.warning(log)
        log = f'WARNING ({str(datetime.now())}): ' + log
        await logs_script(session, user.id, log)
        new_message_text += without_whois_message
        new_reply_markup = keyboard
        # Добавляем скриншот в БД перед сбросом состояния.
        try:
            await orm_add_screenshot(session, data)
            log = 'Скриншот добавлен в БД.'
            logger.info(log)
            log = f'WARNING ({str(datetime.now())}): ' + log
            await logs_script(session, user.id, log)
        except Exception as e:
            log = f'Скриншот не добавлен в БД. Причина: {e}.'
            logger.error(log)
            log = f'ERROR ({str(datetime.now())}): ' + log
            await logs_script(session, user.id, log)
        # Завершаем состояние после отправки скриншота
        await state.clear()
    await message.answer_photo(
        photo=FSInputFile(
            screenshot_path, filename=screenshot_path
        ), caption=new_message_text,
        reply_markup=new_reply_markup
    )
    log = 'Скриншот отправлен в чат.'
    logger.info(log)
    log = f'INFO ({str(datetime.now())}): ' + log
    await logs_script(session, user.id, log)
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
        state: FSMContext,
        session: AsyncSession
):
    """Фунция обработки callback 'Подробнее', при наличии WHOIS"""
    global CHOSEN_LANGUAGE
    await query.answer()
    # Получаем информацию из состояния или из базы данных
    data = await state.get_data()
    info = data.get('info')
    if CHOSEN_LANGUAGE == constants.RU:
        whois_text = f'Информация WHOIS:\n{info}'
        empty_message = 'К сожалению информацию WHOIS добыть не удалось'
        keyboard = ru_keyboard
    else:
        whois_text = f'WHOIS Information:\n{info}'
        empty_message = 'Unfortunately, WHOIS information could not be obtained'
        keyboard = en_keyboard
    if info:
        # Проверка - страховка
        logger.info('Нажата кнопка "Подробнее" к скриншоту.')
        # Отправляем информацию в чат
        await query.message.answer(
            text=whois_text,
            reply_markup=keyboard
        )
    else:
        await query.message.answer(
            text=empty_message,
            reply_markup=keyboard
        )
    # Сбрасываем состояние машины
    await state.clear()
    logger.info('Состояние FSM машины сброшено.')
    # Удаление сообщения с кнопкой "Подробнее"
    await query.message.edit_reply_markup(reply_markup=None)


@user_private_router.message()
async def stub(message: types.Message, session: AsyncSession):
    """Ответ - заглушка на неизвестные команды."""
    # Проверка или добавление пользователя в БД, при выполнении команды
    user = await ensure_user_exists(session, message)
    global CHOSEN_LANGUAGE
    if CHOSEN_LANGUAGE == constants.RU:
        unknown_answer = constants.UNKNOWN_ANSWER_RU
        command_list = constants.COMMAND_LIST_RU
        non_type_answer = constants.NON_TYPE_ANSWER_RU
        keyboard = ru_keyboard
    else:
        unknown_answer = constants.UNKNOWN_ANSWER_EN
        command_list = constants.COMMAND_LIST_EN
        non_type_answer = constants.NON_TYPE_ANSWER_EN
        keyboard = en_keyboard
    if message.text:
        log = (f'{message.from_user.username} - '
               f'ввел несуществующую команду.')
        logger.info(log)
        log = f'INFO ({str(datetime.now())}): ' + log
        await logs_script(session, user.id, log)
        text = message.text
        if text.lower() in constants.GREETINGS_WORDS:
            await hello_cmd(message)
        elif text.lower() in constants.FAREWELL_WORDS:
            await bye_cmd(message)
        else:
            await message.answer(
                f'{unknown_answer}'
                f' <b>{text}</b>\n '
                f'{command_list}',
                reply_markup=keyboard
            )
            await message.answer_animation(constants.UNKNOWN_STICKER)
    else:
        log = (f'{message.from_user.username} - '
               f'отправил не текстовое сообщение.')
        logger.warning(log)
        log = f'WARNING ({str(datetime.now())}): ' + log
        await logs_script(session, user.id, log)
        await message.answer(non_type_answer, reply_markup=keyboard)
        await message.answer_animation(constants.NON_TYPE_STICKER)
