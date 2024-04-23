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

from constants.constants import MAX_SIZE_PICTURE


async def make_shot(date: str, user_id: int, url: str, screenshots_dir: str = 'screenshots'):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    # Получаем Title страницы
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

    if total_height > MAX_SIZE_PICTURE or total_width > MAX_SIZE_PICTURE:
        total_height = total_width = MAX_SIZE_PICTURE

    # Устанавливаем размеры окна браузера, чтобы оно вместило всю страницу
    driver.set_window_size(total_width, total_height)

    # Снимаем скриншот всей страницы
    screenshot = driver.find_element("tag name", "body").screenshot_as_png

    # Закрываем браузер
    driver.quit()

    # Обрезаем скриншот до предельных границ
    image = Image.open(BytesIO(screenshot))
    cropped_image = image.crop((0, 0, total_width, total_height))

    # Очищаем URL и дату для сохранения файла
    cleaned_url = re.sub(r'[^\w\-_]', '', url)
    date_formatted = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f").strftime("%d_%m_%Y")

    # Строим путь к файлу скриншота с помощью os.path.join()
    screenshot_filename = f'user_id_{user_id}_url_{cleaned_url}_date_{date_formatted}.png'
    screenshot_path = os.path.join(screenshots_dir, screenshot_filename)

    # Сохраняем обрезанный скриншот в файл
    with open(screenshot_path, 'wb') as file:
        cropped_image.save(file, "PNG")

    print("Скриншот сохранен по пути:", screenshot_path)
    return screenshot_path, title
