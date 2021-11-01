import RPi.GPIO as io
import time

class Signal:
    def __init__(self, red_pin, green_pin):
        io.setmode(io.BCM)
        self.red_pin = red_pin
        self.green_pin = green_pin
        io.setup(self.red_pin, io.OUT)
        io.setup(self.green_pin, io.OUT)
        self.fast_green = io.PWM(self.green_pin, 10)
        self.fast_red = io.PWM(self.red_pin,10)
        self.red_pwm = io.PWM(self.red_pin, 1)
        self.green_pwm = io.PWM(self.green_pin, 1)

    def _set(self,green, red):
        io.output(self.green_pin, green)
        io.output(self.red_pin, red)

    def fast_blink(self,blocked):
        pin = self.red_pin if blocked else self.green_pin
        io.PWM(pin, 50).start(50

    def show(self, blocked):
        # If blocked, turn off green and turn on red
        self._set(not blocked, blocked)

    def all_off(self):
        self._set(False,False)

    def solid_green(self):
        self._set(True,False)

    def solid_red(self):
        self._set(False, True)

    def fast_green(self):
        self.fast_green(50)

    def fast_red(self):
        self.fast_red(50)

    def alternate(self):
        # LED alternate every half second.
        self.red_pwm.start(50)
        time.sleep(0.5)
        self.green_pwm.start(50)
