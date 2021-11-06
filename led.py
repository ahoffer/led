#! /usr/bin/python3

import time

import RPi.GPIO as io
import requests

from ResettableTimer import ResettableTimer
from signal import Signal

red_pin = 19
green_pin = 26
signal = Signal(red_pin, green_pin)

button_pin = 13
io.setmode(io.BCM)
io.setwarnings(False)
io.setup(button_pin, io.IN, pull_up_down=io.PUD_UP)

youtubeRule = '.*youtube\.com.*'
change_in_progress = False


def isYouTubeBlocked():
    response = requests.get('http://hole:5000/block/regex')
    # print(response.text)
    return 'youtube' in response.text.lower()


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
    # Sleep for at least 100 ms to prevent switch bounce.
    # This sleep could probably be removed if the switch is de-bounced with a capacitor
    # time.sleep(0.15)
    global change_in_progress
    change_in_progress = True
    # print('Detected button push')
    state = isYouTubeBlocked()
    # print(f'Current state={state}')
    newState = not state
    updateYouTubeState(newState)
    change_in_progress = False
    # print(f'Is YouTube blocked: {isYouTubeBlocked()}')


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


signal.blink()
io.add_event_detect(button_pin, io.RISING, callback=button_callback)

one_hour = 60 * 60
timer = ResettableTimer(one_hour, timer_callback)
timer.start()

try:
    while True:
        time.sleep(0.25)
        updateLights()
finally:
    io.cleanup()
