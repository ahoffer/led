from threading import Timer


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
