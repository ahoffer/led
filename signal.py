import RPi.GPIO as io
import time

io.setwarnings(False)

class Signal:
    def __init__(self, red_pin, green_pin):
        io.setmode(io.BCM)
        self.red_pin = red_pin
        self.green_pin = green_pin
        io.setup(self.red_pin, io.OUT)
        io.setup(self.green_pin, io.OUT)
        self.green_pwm = io.PWM(self.green_pin, 10)
        self.red_pwm = io.PWM(self.red_pin, 10)

    def _set(self, green, red):
        io.output(self.green_pin, green)
        io.output(self.red_pin, red)

    def fast_blink(self, blocked):
        if blocked:
            self.red_pwm.ChangeFrequency(50)
            self.start(50)
        else:
            self.green_pwm.ChangeFrequency(50)
            self.start(50)

    def show(self, blocked):
        # If blocked, turn off green and turn on red
        self._set(not blocked, blocked)

    def all_off(self):
        self._set(False, False)

    def solid_green(self):
        self._set(True, False)

    def solid_red(self):
        self._set(False, True)

    def fast_green(self):
        self.green_pwm(50)

    def fast_red(self):
        self.red_pwm(50)

    def alternate(self):
        # Alternate LED every half second.
        self.red_pwm.ChangeFrequency(1)
        self.red_pwm.start(50)
        time.sleep(0.5)
        self.green_pwm.ChangeFrequency(1)
        self.green_pwm.start(50)
