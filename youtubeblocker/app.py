import os
import time
from sys import stderr

import RPi.GPIO as io
from loguru import logger
from piholeclient.controllers import YouTubeRule

from .controllers import LampController, ButtonController, ResettableTimer

POLLING_SECONDS = 0.25

ONE_HOUR = 60 * 60


class Application():

    def __init__(self, client):
        # Cleanup in case your having been fiddling around in a console.
        io.cleanup()
        io.setwarnings(False)
        io.setmode(io.BCM)
        red_pin = int(os.getenv('RED_PIN'))
        green_pin = int(os.getenv('GREEN_PIN'))
        button_pin = int(os.getenv('BUTTON_HIGH_PIN'))
        fallback_seconds = int(os.getenv('FALLBACK_SECONDS', ONE_HOUR))
        logger.info(f'Red LED pin={red_pin}')
        logger.info(f'Green LED pin={green_pin}')
        logger.info(f'Button pin={button_pin}')
        logger.info(f'Fallback seconds={fallback_seconds}')
        self.lamps = LampController(red_pin, green_pin)
        self.button = ButtonController(button_pin, self.button_callback)
        self.youtube = YouTubeRule(client)
        self.change_in_progress = False
        self.deadman_switch = ResettableTimer(fallback_seconds, self.timer_callback)

    def update_lamps(self):
        try:
            if self.youtube.youtube_is_blocked():
                if self.change_in_progress:
                    logger.trace('Set red lamp to fast')
                    self.lamps.fast_red()
                else:
                    logger.trace('Set red lamp to solid')
                    self.lamps.solid_red()
            else:
                if self.change_in_progress:
                    logger.trace('Set green lamp to fast')
                    self.lamps.fast_green()
                else:
                    logger.trace('Set green lamp to solid')
                    self.lamps.solid_green()
        except Exception as e:
            logger.warning('Blinking lamps')
            self.lamps.blink()

    def event_loop(self):
        try:
            while True:
                time.sleep(POLLING_SECONDS)
                self.update_lamps()
        finally:
            io.cleanup()

    def button_callback(self, channel):
        self.change_in_progress = True
        logger.info('Detected button push', file=stderr)
        try:
            logger.info(f'Attempting to set BLOCKED={not self.youtube.youtube_is_blocked()}')
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
