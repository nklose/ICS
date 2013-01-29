""" To use:
    - Import first in main.
"""
import logging
from logging.handlers import RotatingFileHandler

FORMAT = '[%(asctime)s] %(levelname)s [%(name)s] ' + \
    '<%(threadName)s>: %(message)s'
DATE_FMT = '%I:%M:%S %p'

logging.basicConfig(level=logging.DEBUG,
                    format=FORMAT,
                    datefmt=DATE_FMT)
# create console handler and set level to debug
#ch = logging.StreamHandler()
#ch.setLevel(logging.DEBUG)
# 2 MB rotating files, up to three.
rfh = RotatingFileHandler("ics.log", maxBytes=2097152, backupCount=3)
rfh.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter(FORMAT, datefmt=DATE_FMT)
#ch.setFormatter(formatter)
rfh.setFormatter(formatter)
#logging.getLogger('').addHandler(ch)
logging.getLogger('').addHandler(rfh)
logging.info("=== Started Logger ===")
