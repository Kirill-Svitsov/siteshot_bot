import unittest
from unittest.mock import patch, AsyncMock
from datetime import datetime

from constants.constants import (
    TEST_USER_ID,
    OK_STATUS_CODE,
    NOT_FOUND_STATUS_CODE
)
from utils import make_shot


class TestMakeShot(unittest.TestCase):
    """Тестирование функции получения скриншота и WHOIS"""

    @patch('requests.get')
    @patch('selenium.webdriver.Chrome')
    @patch('whois.whois')
    async def test_make_shot(self, mock_whois, mock_driver, mock_get):
        """Тестируем make_shot на верных данных"""
        mock_response = AsyncMock()
        mock_response.status_code = OK_STATUS_CODE
        mock_response.content = (
            b'<html><title>Test Title</title><body>Test Body</body></html>'
        )
        mock_get.return_value = mock_response
        mock_whois.return_value = {'domain_name': 'test.com'}
        mock_driver_instance = mock_driver.return_value
        mock_driver_instance.find_element.return_value.screenshot_as_png = (
            b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'
        )
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        user_id = TEST_USER_ID
        url = 'https://example.com'
        result = await make_shot.make_shot(date, user_id, url)
        # Проверяем, что функция вернула ожидаемые значения
        self.assertEqual(result[1], 'Test Title')
        self.assertEqual(result[2]['domain_name'], 'test.com')

    @patch('requests.get')
    async def test_make_shot_invalid_status_code(self, mock_get):
        """Тестируем функцию с неверным статус кодом ответа"""
        mock_response = AsyncMock()
        mock_response.status_code = NOT_FOUND_STATUS_CODE
        mock_get.return_value = mock_response
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        user_id = TEST_USER_ID
        url = 'invalid_url'
        result = await make_shot.make_shot(date, user_id, url)
        self.assertEqual(result[0], 'Error: Invalid URL')

    @patch('whois.whois')
    async def test_make_shot_unable_to_get_whois(self, mock_whois):
        """Тестируем функцию с недоступным WHOIS"""
        mock_whois.side_effect = Exception("Unable to get whois info")
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        user_id = TEST_USER_ID
        url = 'https://example.com'
        result = await make_shot.make_shot(date, user_id, url)
        self.assertEqual(result[0], 'Error: Unable to get whois info')


if __name__ == '__main__':
    unittest.main()
