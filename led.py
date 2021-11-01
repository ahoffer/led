#! /usr/bin/python3

import RPi.GPIO as io
import time
import requests

red_light = 19
green_light = 26
button = 13
io.setmode(io.BCM)
io.setwarnings(False)
io.setup(red_light, io.OUT)
io.setup(green_light, io.OUT)
io.setup(button, io.IN, pull_up_down=io.PUD_UP)
#io.setup(button, io.IN, pull_up_down=io.PUD_DOWN)

youtubeRule = '.*youtube\.com.*'

def set(channel, on):
    if on:
        io.output(channel, io.HIGH)
    else:
        io.output(channel, io.LOW)

def isYouTubeBlocked():
    response = requests.get('http://hole:5000/block/regex')
    #print(response.text)
    if 'youtube' in response.text.lower():
        return True
    else:
        return False

def signalYouTubeStatus():
    blocked = isYouTubeBlocked()
    set(red_light, blocked)
    set(green_light, not blocked)

def button_callback(channel):
    time.sleep(0.15)
    print('Detected button push')
    state = isYouTubeBlocked()
    #print(f'Current state={state}')
    newState = not state
    updateYouTubeState(newState)
    #print(f'Is YouTube blocked: {isYouTubeBlocked()}')

def updateYouTubeState(enableBlock):
    #print(f'updateYouTubeState({enableBlock})')
    if enableBlock:
        r = requests.put('http://hole:5000/block/regex', data=youtubeRule)
    else:
        r = requests.delete('http://hole:5000/block/regex', data=youtubeRule)
    #print(r.text)

io.add_event_detect(button,io.RISING,callback=button_callback) 

try:
    while True:
        time.sleep(0.10)
        signalYouTubeStatus()
finally:
    io.output(red_light, 0)
    io.output(green_light, 0)
