import os
from datetime import datetime
import re

from io import BytesIO
from playwright.async_api import async_playwright
from PIL import Image
import whois

from constants.constants import (
    SCREENSHOTS_DIR,
    MAX_SIZE_PICTURE
)
from utils.loger import logger


async def make_shot(date: str, user_id: int, url: str):
    """Асинхронная функция для получения скриншота и Title
     сайта с использованием playwright."""
    # Проверяем, существует ли директория screenshots,
    # если нет, создаем ее
    if not os.path.exists(SCREENSHOTS_DIR):
        os.makedirs(SCREENSHOTS_DIR)
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url)
            title = await page.title() or 'Не удалось получить title'
            screenshot = await page.screenshot(full_page=True)
            if screenshot:
                logger.info('Скриншот получен')
                # Создаем объект изображения из скриншота
                image = Image.open(BytesIO(screenshot))
                # Проверяем размеры изображения
                width, height = image.size
                if width > MAX_SIZE_PICTURE or height > MAX_SIZE_PICTURE:
                    logger.info(
                        'Размеры скриншота превышают допустимые.'
                    )
                    # Обрезаем изображение до максимально допустимых размеров
                    image = image.resize(
                        (min(width, MAX_SIZE_PICTURE),
                         min(height, MAX_SIZE_PICTURE))
                    )
                # Сохраняем скриншот в файл
                cleaned_url = re.sub(r'[^\w\-_]', '', url)
                date_formatted = datetime.strptime(
                    date, "%Y-%m-%d %H:%M:%S.%f"
                ).strftime("%d_%m_%Y")
                screenshot_filename = (f'user_id_{user_id}'
                                       f'_url_{cleaned_url}'
                                       f'_date_{date_formatted}.png')
                screenshot_path = os.path.join(
                    SCREENSHOTS_DIR,
                    screenshot_filename
                )
                image.save(screenshot_path)
                logger.info(f'Скриншот сохранен по пути {screenshot_path}.')
                try:
                    whois_info = whois.whois(url)
                    if whois_info:
                        logger.info('WHOIS получен и отправлен в чат.')
                        await browser.close()
                        return screenshot_path, title, whois_info
                except Exception as e:
                    logger.error(
                        f'Функция make_shot не получила WHOIS.'
                        f'Причина - {e}.'
                    )
                    await browser.close()
                    return screenshot_path, title
            else:
                logger.error('Не удалось получить скриншот')
                await browser.close()
                return
    except Exception as e:
        logger.error(f'Ошибка при получении скриншота: {e}')
        return
