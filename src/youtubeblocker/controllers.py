import time
from threading import Timer

import RPi.GPIO as io


class LampController(object):
    def __init__(self, red_pin, green_pin):
        self.red_pin = red_pin
        self.green_pin = green_pin
        io.setup(self.red_pin, io.OUT)
        io.setup(self.green_pin, io.OUT)
        self.green_pwm = io.PWM(self.green_pin, 1)
        self.red_pwm = io.PWM(self.red_pin, 1)

    def _set(self, pwm, hertz=1, duty_cycle=100):
        pwm.ChangeFrequency(hertz)
        pwm.start(duty_cycle)

    def _set_fast(self, pwm):
        self._set(pwm, 5, 50)

    def _set_solid(self, pwm):
        self._set(pwm, 50, 100)

    def _green_off(self):
        self._set(self.green_pwm, duty_cycle=0)

    def _red_off(self):
        self._set(self.red_pwm, duty_cycle=0)

    def blink(self):
        # Alternate LED every half second.
        # print('BLINK')
        self._set(self.red_pwm, 2, 50)
        time.sleep(0.5)
        self._set(self.green_pwm, 2, 50)

    def solid_green(self):
        # print('SOLID GREEN')
        self._red_off()
        self._set(self.green_pwm, 100, 100)

    def solid_red(self):
        # print('SOLID RED')
        self._green_off()
        self._set_solid(self.red_pwm)

    def fast_green(self):
        # print('FAST GREEN')
        self._red_off()
        self._set_fast(self.green_pwm)

    def fast_red(self):
        self._green_off()
        self._set_fast(self.red_pwm)

    def all_off(self):
        self._green_off()
        self._red_off()


class ButtonController:
    # Connect one pole of the button to the pin, connect
    # the other pole to GND
    def __init__(self, pin, button_callback):
        io.setup(pin, io.IN, pull_up_down=io.PUD_UP)
        # The event_detect does some debouncing, but the breadboard still
        # needed 1 nF capacitor across the across the button's poles.
        io.add_event_detect(pin, io.RISING, callback=button_callback)


class ResettableTimer(object):
    def __init__(self, interval, function, args=None):
        self.interval = interval
        self.function = function
        self.args = args
        self.timer = None

    def reset(self):
        self.cancel()
        self.timer = Timer(self.interval, self.function, self.args)
        self.timer.daemon = True
        self.timer.start()

    def cancel(self):
        if self.timer:
            self.timer.cancel()
