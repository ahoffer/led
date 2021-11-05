import time

import RPi.GPIO as io

io.setwarnings(False)

class Signal:
    def __init__(self, red_pin, green_pin):
        io.setmode(io.BCM)
        self.red_pin = red_pin
        self.green_pin = green_pin
        io.setup(self.red_pin, io.OUT)
        io.setup(self.green_pin, io.OUT)
        self.green_pwm = io.PWM(self.green_pin, 1)
        self.red_pwm = io.PWM(self.red_pin, 1)


    def _set(self, pwm, duty_cycle=100, hertz=1):
        pwm.ChangeFrequency(hertz)
        pwm.start(duty_cycle)


    def _green_off(self):
        self._set(self.green_pwm, 0)


    def _red_off(self):
        self._set(self.red_pwm, 0)


    def blink(self):
        # Alternate LED every half second.
        print('BLINK')
        self._set(self.red_pwm, 50)
        time.sleep(0.5)
        self._set(self.green_pwm, 50)


    def solid_green(self):
        self._red_off(self)
        self._set(self.green_pwm, 100)


    def solid_red(self):
        print('SOLID RED')
        self._green_off(self)
        self._set(self.red_pwm, 100)


    def fast_green(self):
        self._red_off()
        self._set(self.green_pwm, 50, 50)


    def fast_red(self):
        self._green_off()
        self._set(self.red_pwm, 50, 50)
