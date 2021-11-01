#! /usr/bin/python3

import RPi.GPIO as io
import time
import requests

red_light_pin = 19
green_light_pin = 26
button_pin = 13
io.setmode(io.BCM)
io.setwarnings(False)
io.setup(red_light_pin, io.OUT)
io.setup(green_light_pin, io.OUT)
io.setup(button_pin, io.IN, pull_up_down=io.PUD_UP)


io.output(red_light_pin, 0)
io.output(green_light_pin,0)

pwm_r = io.PWM(red_light_pin, 1)
pwm_g = io.PWM(green_light_pin, 1)

def alternate():
    pwm_r.start(50)
    time.sleep(0.5)
    pwm_g.start(50)

alternate()

try:
    while 1:
        time.sleep(1)
finally:
    io.cleanup()
