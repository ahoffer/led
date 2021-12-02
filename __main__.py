import os

from piholeclient.models import Pihole

from app import Application

Application(Pihole('192.168.0.2', os.getenv('PI_PASSWD'))).run()
