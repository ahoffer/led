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

def isYouTubeBlocked():
    response = requests.get('http://hole:5000/block/regex')
    if DEBUG:
        pass
        # print(response.text)
    return 'youtube' in response.text.lower()

def signalYouTubeStatus():
    try:
        blocked = isYouTubeBlocked()
        if DEBUG:
            print(f'youtube is blocked == {blocked}')
        signal.show(blocked)
    except:
        signal.alternate()

def button_callback(channel):
    # Sleep for at least 100 ms to prevent switch bounce.
    # This sleep could probably be removed if the switch is de-bounced with a capacitor
    # time.sleep(0.15)
    if DEBUG:
        print('Detected button push')
    state = isYouTubeBlocked()
    # print(f'Current state={state}')
    signal.fast_blink(state)
    time.sleep(5)
    newState = not state
    updateYouTubeState(newState)
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
        signal.alternate()

signal.alternate()

io.add_event_detect(button_pin, io.RISING, callback=button_callback)

print('Entering loop')
try:
    while True:
        time.sleep(0.5)
        signalYouTubeStatus()
finally:
    io.cleanup()
