import logging
from logging.handlers import RotatingFileHandler
import os

from constants.constants import LOGS_DIR

# Создаем директорию для логов, если ее нет
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)
# Инициализация логгера
logger = logging.getLogger(__name__)
FORMAT = '%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) [%(filename)s]'
logger.setLevel(logging.INFO)
# Формируем консольный логгер
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter(FORMAT))
stream_handler.setLevel(logging.INFO)
# Формируем файловый логгер
file_handler = RotatingFileHandler('logs/logs.log', encoding='utf-8')
file_handler.setFormatter(logging.Formatter(FORMAT))
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
