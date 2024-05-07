import logging
from pythonjsonlogger import jsonlogger
from src.api.core.config import settings


def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(settings.LOG_LEVEL)
    logger.handlers = []

    log_format = "%(asctime)s %(name)s %(levelname)s %(message)s"
    json_formatter = jsonlogger.JsonFormatter(log_format)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(json_formatter)
    console_handler.setLevel(settings.LOG_LEVEL)

    logger.addHandler(console_handler)
