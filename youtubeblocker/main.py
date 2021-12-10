import os

from loguru import logger
from piholeclient.models import Pihole

from youtubeblocker.app import Application

logger.info('Starting application')
Application(Pihole('192.168.0.2', os.getenv('PI_PASSWD'))).run()
