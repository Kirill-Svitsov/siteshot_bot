import os
from datetime import datetime
import re
import asyncio
from playwright.async_api import async_playwright
import aiohttp
import whois

from constants.constants import SCREENSHOTS_DIR, VALID_STATUS_CODES
from utils.loger import logger


async def make_shot(date: str, user_id: int, url: str):
    """Асинхронная функция для получения скриншота и Title сайта с использованием playwright."""
    # Проверяем, существует ли директория screenshots, если нет, создаем ее
    if not os.path.exists(SCREENSHOTS_DIR):
        os.makedirs(SCREENSHOTS_DIR)

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status in VALID_STATUS_CODES:
                        await page.goto(url)
                        title = await page.title() or 'Не удалось получить title'
                        screenshot = await page.screenshot(full_page=True)
                    else:
                        logger.error(
                            f'Неверный статус код ответа при получении информации по URL {url}: {response.status}')
                        await browser.close()
                        return None

            await browser.close()

        # Проверяем, был ли успешно получен скриншот
        if screenshot:
            logger.info('Скриншот получен')
            # Сохраняем скриншот в файл
            cleaned_url = re.sub(r'[^\w\-_]', '', url)
            date_formatted = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f").strftime("%d_%m_%Y")
            screenshot_filename = f'user_id_{user_id}_url_{cleaned_url}_date_{date_formatted}.png'
            screenshot_path = os.path.join(SCREENSHOTS_DIR, screenshot_filename)
            with open(screenshot_path, 'wb') as file:
                file.write(screenshot)
                logger.info(f'Скриншот сохранен по пути {screenshot_path}.')
            try:
                whois_info = whois.whois(url)
                if whois_info:
                    logger.info('WHOIS получен и отправлен в чат.')
                    return screenshot_path, title, whois_info
            except Exception as e:
                logger.error(
                    f'Функция make_shot не получила WHOIS.'
                    f'Причина - {e}.'
                )
                return screenshot_path, title
        else:
            logger.error('Не удалось получить скриншот')
            return None

    except Exception as e:
        logger.error(f'Ошибка при получении скриншота: {e}')
        return None
