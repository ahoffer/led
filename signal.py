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

    def _set_fast(self, pwm):
        self._set(pwm, 50, 5)


    def _set_solid(self, pwm):
        self._set(pwm, 100, 50)


    def _green_off(self):
        self._set(self.green_pwm, 0)


    def _red_off(self):
        self._set(self.red_pwm, 0)


    def blink(self):
        # Alternate LED every half second.
        print('BLINK')
        self._set(self.red_pwm, 50, 2)
        time.sleep(0.5)
        self._set(self.green_pwm, 50, 2)


    def solid_green(self):
        print('SOLID GREEN')
        self._red_off()
        self._set(self.green_pwm, 100, 100)


    def solid_red(self):
        print('SOLID RED')
        self._green_off()
        self._set_solid(self.red_pwm)


    def fast_green(self):
        print('FAST GREEN')
        self._red_off()
        self._set_fast(self.green_pwm)


    def fast_red(self):
        self._green_off()
        self._set_fast(self.red_pwm)
