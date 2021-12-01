from threading import Timer


class ResettableTimer(object):
    def __init__(self, interval, function, args=None):
        self.interval = interval
        self.function = function
        self.args = args
        self._make_timer()

    def _make_timer(self):
        self.timer = Timer(self.interval, self.function, self.args)

    def start(self):
        self.timer.start()

    def reset(self):
        self.timer.cancel()
        self._make_timer()
        self.timer.daemon = True
        self.timer.start()
