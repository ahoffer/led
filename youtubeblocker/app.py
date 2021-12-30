import os
import time
from sys import stderr

import RPi.GPIO as io
from loguru import logger
from piholeclient.controllers import YouTubeRule

from .controllers import LampController, ButtonController, ResettableTimer


class Application():

    def __init__(self, client):
        # Cleanup in case your having been fiddling around in a console.
        io.cleanup()
        io.setwarnings(False)
        io.setmode(io.BCM)
        self.lamps = LampController(red_pin=os.getenv('RED_PIN'), green_pin=os.getenv('GREEN_PIN'))
        self.button = ButtonController(os.getenv('BUTTON_HIGH_PIN'), self.button_callback)
        self.youtube = YouTubeRule(client)
        self.change_in_progress = False
        self.deadman_switch = ResettableTimer(os.getenv('FALLBACK_SECONDS'), self.timer_callback)

    def update_lamps(self):
        try:
            if self.youtube.youtube_is_blocked():
                if self.change_in_progress:
                    logger.debug('Set red lamp to fast')
                    self.lamps.fast_red()
                else:
                    logger.debug('Set red lamp to solid')
                    self.lamps.solid_red()
            else:
                if self.change_in_progress:
                    logger.debug('Set green lamp to fast')
                    self.lamps.fast_green()
                else:
                    logger.debug('Set green lamp to solid')
                    self.lamps.solid_green()
        except Exception as e:
            logger.warning('Blinking lamps')
            self.lamps.blink()

    def event_loop(self):
        try:
            while True:
                time.sleep(0.25)
                self.update_lamps()
        finally:
            io.cleanup()

    def button_callback(self, channel):
        self.change_in_progress = True
        logger.info('Detected button push', file=stderr)
        try:
            self.youtube.flip()
            self.deadman_switch.reset()
        except:
            self.lamps.blink()
        self.change_in_progress = False

    def timer_callback(self):
        # Fall back to blocking YouTube.
        logger.info('Timeout. Fallback to blocking youtube')
        self.youtube.block()
        self.deadman_switch.reset()

    def run(self):
        # Show the program started by blinking the lights.
        self.lamps.blink()
        # In the case the program just restarted, start the deadman switch countdown
        self.deadman_switch.reset()
        # Loop forever
        self.event_loop()
