""" To use:
    - Import this file first in main.
    import icsLogger
    - Import logging wherever you need to log information
    import logging
    - add at top of the module
    LOGGER = use logging.getLogger('module')

Copryight (c) 2013 Nick Klose, Richard Leung, Cameron Mann, Glen Nelson, Omar
Qadri, and James Wang under the 401 IP License.

This Agreement, effective the 1st day of April 2013, is entered into by and
between Dr. Nils Petersen (hereinafter "client") and the students of the
Biomembrane team (hereinafter "the development team"), in order to establish
terms and conditions concerning the completion of the Image Correlation
Spectroscopy application (hereinafter "The Application") which is limited to the
application domain of application-domain (hereinafter "the domain of use for the
application").  It is agreed by the client and the development team that all
domain specific knowledge and compiled research is the intellectual property of
the client, regarded as a copyrighted collection. The framework and code base
created by the development team is their own intellectual property, and may only
be used for the purposes outlined in the documentation of the application, which
has been provided to the client. The development team agrees not to use their
framework for, or take part in the development of, anything that falls within
the domain of use for the application, for a period of 6 (six) months after the
signing of this agreement.
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
