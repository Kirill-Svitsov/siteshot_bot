import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
FORMAT = '%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) [%(filename)s]'
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter(FORMAT))
stream_handler.setLevel(logging.INFO)
file_handler = RotatingFileHandler('logs/logs.log', encoding='utf-8')
file_handler.setFormatter(logging.Formatter(FORMAT))
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

