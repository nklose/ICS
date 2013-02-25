""" To use:
    - Import first in main.
"""
import logging
from logging.handlers import RotatingFileHandler

FORMAT = '[%(asctime)s] %(levelname)s [%(name)s] ' + \
    '<%(threadName)s>: %(message)s'
DATE_FMT = '%I:%M:%S %p'

logger = logging.getLogger('')
logger.setLevel(logging.DEBUG)

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.INFO)

# 2 MB rotating files, up to three.
rotatingFileHandler = RotatingFileHandler("ics.log", maxBytes=2097152,
                                          backupCount=3)
rotatingFileHandler.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter(FORMAT, datefmt=DATE_FMT)
rotatingFileHandler.setFormatter(formatter)
consoleHandler.setFormatter(formatter)

logger.addHandler(rotatingFileHandler)
logger.addHandler(consoleHandler)
logging.debug("=== Started Logger ===")
