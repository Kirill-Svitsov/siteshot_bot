import os
from datetime import datetime
import re
import requests

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from PIL import Image
from io import BytesIO
import whois

from constants.constants import MAX_SIZE_PICTURE, VALID_STATUS_CODES, HEADERS
from utils.loger import logger


async def make_shot(date: str, user_id: int, url: str, screenshots_dir: str = 'screenshots'):
    """Функция получения и возвращения скриншота и Title сайта.
    Так как selenium работает синхронно, эта функция блокирует поток
    и не позволяет другим функциям обрабатывать запросы.
    """
    # Проверяем, существует ли директория screenshots, если нет, создаем ее
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)

    response = requests.get(url, headers=HEADERS)
    logger.info(f'Функция make_shot начала работу.')
    logger.info(f'Функция make_shot получила ответ: {response.status_code}')
    if response.status_code not in VALID_STATUS_CODES:
        logger.warning(f'Функция make_shot не смогла получить доступ к странице.')
        return
    # Получаем Title страницы
    logger.info(f'Функция make_shot получила доступ к странице.')
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('title').text
    # Создаем объект опций для настройки браузера
    options = Options()
    options.add_argument("--no-sandbox")  # Необязательно
    options.add_argument("--headless")  # Необязательно
    # Инициализируем драйвер с помощью ChromeDriverManager
    service = Service()
    driver = webdriver.Chrome(options=options, service=service)
    driver.get(url)
    # Получаем размеры страницы
    total_width = driver.execute_script("return document.body.offsetWidth")
    total_height = driver.execute_script("return document.body.scrollHeight")
    # Проверка на допустимые значения изображения в Telegram
    if total_height > MAX_SIZE_PICTURE or total_width > MAX_SIZE_PICTURE:
        logger.info(f'Размеры скриншота превышают допустимые.')
        total_height = total_width = MAX_SIZE_PICTURE
    else:
        logger.info(f'Размеры скриншота проходят/')
    # Устанавливаем размеры окна браузера, чтобы оно вместило всю страницу
    driver.set_window_size(total_width, total_height)
    # Снимаем скриншот всей страницы
    screenshot = driver.find_element("tag name", "body").screenshot_as_png
    # Закрываем браузер
    driver.quit()
    # Форматируем
    image = Image.open(BytesIO(screenshot))
    # Очищаем URL и дату для сохранения файла
    cleaned_url = re.sub(r'[^\w\-_]', '', url)
    date_formatted = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f").strftime("%d_%m_%Y")
    # Строим путь к файлу скриншота с помощью os.path.join()
    screenshot_filename = f'user_id_{user_id}_url_{cleaned_url}_date_{date_formatted}.png'
    screenshot_path = os.path.join(screenshots_dir, screenshot_filename)
    # Сохраняем обрезанный скриншот в файл
    with open(screenshot_path, 'wb') as file:
        image.save(file, "PNG")
        logger.info(f'Скриншот сохранен по пути {screenshot_path}.')
    try:
        info = whois.whois(url)
        if info:
            logger.info('Функция make_shot получила WHOIS.')
            return screenshot_path, title, info
    except Exception as e:
        logger.error(f'Функция make_shot не получила WHOIS. Причина - {e}.')
    return screenshot_path, title