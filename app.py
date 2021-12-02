#! /usr/bin/python3
import time

import RPi.GPIO as io
from piholeclient.controllers import YouTubeRule

from ResettableTimer import ResettableTimer
from controllers import LampController, ButtonController


class Application():

    def __init__(self, client):
        io.setwarnings(False)
        io.setmode(io.BCM)
        self.lamps = LampController(red_pin=19, green_pin=26)
        self.button = ButtonController(13, self.button_callback)
        self.youtube = YouTubeRule(client)
        self.change_in_progress = False
        # After 1 hour, revert to blocking the site.
        one_hour = 60 * 60
        self.deadman_switch = ResettableTimer(one_hour, self.timer_callback)

    def update_lamps(self):
        try:
            if self.youtube.youtube_is_blocked():
                if self.change_in_progress:
                    self.lamps.fast_red()
                else:
                    self.lamps.solid_red()
            else:
                if self.change_in_progress:
                    self.lamps.fast_green()
                else:
                    self.lamps.solid_green()
        except:
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
        # print('Detected button push')
        try:
            self.youtube.flip()
            self.deadman_switch.reset()
        except:
            self.lamps.blink()
        self.change_in_progress = False

    def timer_callback(self):
        # Fall back to blocking YouTube.
        self.youtube.block()
        self.deadman_switch.reset()

    def run(self):
        # Show the program started by blinking the lights.
        self.lamps.blink()
        # In the case the program just restarted, start the deadman switch countdown
        self.deadman_switch.reset()
        # Loop forever
        self.event_loop()
