import os
import sys

from loguru import logger
from piholeclient.models import Pihole

from youtubeblocker.app import Application

# Remove default sink before adding a new one
logger.remove()
log_level = os.getenv("LOG_LEVEL", "INFO")
logger.add(sys.stderr, format="{level} {message}", level=log_level)
logger.info(f'Log level={log_level}')

logger.info('Starting application')
Application(Pihole('192.168.0.2', os.getenv('PI_PASSWD'))).run()
