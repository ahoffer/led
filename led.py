#! /usr/bin/python3
import os
import time

import RPi.GPIO as io
from piholeclient.controllers import YouTubeRule
from piholeclient.models import Pihole

from ResettableTimer import ResettableTimer
from signal import Signal

# Map actual pin configuration to variables to create the signal object.
signal = Signal(red_pin=19, green_pin=26)

# Set up button.
button_pin = 13
io.setmode(io.BCM)
io.setwarnings(False)
io.setup(button_pin, io.IN, pull_up_down=io.PUD_UP)

# Set up Pi-hole client
client = Pihole('192.168.0.2', os.getenv('PI_PASSWD'))
rule = YouTubeRule(client)

# Set global state
change_in_progress = False


def isYouTubeBlocked():
    return rule.youtube_is_blocked()


def updateLights():
    try:
        blocked = isYouTubeBlocked()
        # print(f'blocked=={blocked}, changing=={change_in_progress}')
        if blocked:
            if change_in_progress:
                signal.fast_red()
            else:
                signal.solid_red()
        else:
            if change_in_progress:
                signal.fast_green()
            else:
                signal.solid_green()
    except:
        signal.blink()


def button_callback(channel):
    global change_in_progress
    global rule
    change_in_progress = True
    # print('Detected button push')
    try:
        rule.flip()
    except:
        signal.blink()
    change_in_progress = False
    # print(f'Is YouTube blocked: {isYouTubeBlocked()}')


def timer_callback():
    global timer
    global rule
    timer.reset()
    rule.block()


# Start executable code.
# Show the program started by blinking the lights.
signal.blink()

# Create button callback
io.add_event_detect(button_pin, io.RISING, callback=button_callback)

# After 1 hour, revert to blocking the site.
one_hour = 60 * 60
timer = ResettableTimer(one_hour, timer_callback)
timer.start()

try:
    while True:
        time.sleep(0.25)
        updateLights()
finally:
    io.cleanup()
