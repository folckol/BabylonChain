import os
import time
from sys import stderr

from loguru import logger

logger.remove()
logger.add(stderr, format='<white>{time:HH:mm:ss}</white>'
                          ' | <level>{level: <8}</level>'
                          ' | <white>{message}</white>')

logger.add("LogsBackUp/logs.log", format='<white>{time:HH:mm:ss}</white>'
                                   ' | <level>{level: <8}</level>'
                                   ' -| <white>{message}</white>')

