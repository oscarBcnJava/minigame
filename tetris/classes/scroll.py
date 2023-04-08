DELAY_TIME_MS = 1000
AUTO_DOWN_DELAY_TIME_MS = 100

class Scroll:
    def __init__(self, level, ticks):
        self.level = level
        self.delay = DELAY_TIME_MS
        self.ticks = ticks

    def is_allowed_scroll(self, actual_ticks, auto_down = False):
        if auto_down: 
            self.delay = AUTO_DOWN_DELAY_TIME_MS
        else:
            self.delay = DELAY_TIME_MS
        if actual_ticks > self.ticks + (self.delay / self.level):
            self.ticks = actual_ticks
            return True
        return False