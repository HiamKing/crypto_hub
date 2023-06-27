import logging
from logging.handlers import RotatingFileHandler


def get_logger(name: str, path: str) -> logging.Logger:
    formatter = logging.Formatter(
        '%(asctime)s,%(msecs)d <%(name)s>[%(levelname)s]: %(message)s',
        '%H:%M:%S')
    handler = RotatingFileHandler(path, maxBytes=104857600, backupCount=10)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    return logger
