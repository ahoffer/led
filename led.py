#! /usr/bin/python3

import RPi.GPIO as io
import time
import requests
from signal import Signal

DEBUG = True

red_pin = 19
green_pin = 26
signal = Signal(red_pin,green_pin)

button_pin = 13
io.setmode(io.BCM)
io.setwarnings(False)
io.setup(button_pin, io.IN, pull_up_down=io.PUD_UP)

youtubeRule = '.*youtube\.com.*'
change_in_progress = False

def isYouTubeBlocked():
    response = requests.get('http://hole:5000/block/regex')
    if DEBUG:
        pass
        # print(response.text)
    return 'youtube' in response.text.lower()

def updateLights():
    try:
        blocked = isYouTubeBlocked()
        if DEBUG:
            print(f'blocked=={blocked}, changing=={change_in_progress}')
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
        pass
        # signal.blink()

def button_callback(channel):
    # Sleep for at least 100 ms to prevent switch bounce.
    # This sleep could probably be removed if the switch is de-bounced with a capacitor
    # time.sleep(0.15)
    global change_in_progress
    change_in_progress = True
    if DEBUG:
        print('Detected button push')
    state = isYouTubeBlocked()
    updateLights()
    # print(f'Current state={state}')
    newState = not state
    updateYouTubeState(newState)
    change_in_progress = False
    # print(f'Is YouTube blocked: {isYouTubeBlocked()}')

def updateYouTubeState(block):
    try:
        #print(f'updateYouTubeState({enableBlock})')
        if block:
            r = requests.put('http://hole:5000/block/regex', data=youtubeRule)
        else:
            r = requests.delete('http://hole:5000/block/regex', data=youtubeRule)
        #print(r.text)
    except:
        pass
        # signal.blink()

signal.blink()
io.add_event_detect(button_pin, io.RISING, callback=button_callback)

print('Entering loop')
try:
    while True:
        time.sleep(0.5)
        updateLights()
finally:
    io.cleanup()
