#! /usr/bin/python3

import time
import logging

import RPi.GPIO as io
import requests
from logging.handlers import RotatingFileHandler
from ResettableTimer import ResettableTimer
from signal import Signal

red_pin = 19
green_pin = 26
signal = Signal(red_pin, green_pin)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(filename='led.log',maxBytes=1024*256,backupCount=2)
logger.addHandler(handler)
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", "%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)

button_pin = 13
io.setmode(io.BCM)
io.setwarnings(False)
io.setup(button_pin, io.IN, pull_up_down=io.PUD_UP)

youtubeRule = '.*youtube\.com.*'
change_in_progress = False


def isYouTubeBlocked():
    response = requests.get('http://hole:5000/block/regex')
    # YouTube is blocked if it is in the list of rules and the rule is enabled.
    #print(response.text)
    blocked = [line for line in response.text.split('\n') if "youtube" in line and "enabled" in line]
    return blocked


def updateLights():
    try:
        blocked = isYouTubeBlocked()
        logger.debug(f'blocked=={blocked}, changing=={change_in_progress}')
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
    change_in_progress = True
    logger.info('Detected button push')
    state = isYouTubeBlocked()
    newState = not state
    updateYouTubeState(newState)
    change_in_progress = False


def updateYouTubeState(block):
    try:
        # print(f'updateYouTubeState({enableBlock})')
        if block:
            r = requests.put('http://hole:5000/block/regex', data=youtubeRule)
        else:
            r = requests.delete('http://hole:5000/block/regex', data=youtubeRule)
        # print(r.text)
    except:
        signal.blink()


def timer_callback():
    global timer
    timer.reset()
    updateYouTubeState(True)

logger.info('Start')
signal.blink()

# Register function to call when button is pressed
io.add_event_detect(button_pin, io.RISING, callback=button_callback)

# Set up timer to turn off YouTube if left on for too long
one_hour = 60 * 60
timer = ResettableTimer(one_hour, timer_callback)
timer.start()

try:
    while True:
        time.sleep(0.25)
        updateLights()
finally:
    signal.all_off()
    logger.info('End')
    io.cleanup()
