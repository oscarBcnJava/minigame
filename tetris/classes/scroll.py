class Scroll:
    def __init__(self, level, delay, ticks):
        self.level = level
        self.delay = delay
        self.ticks = ticks

    def is_allowed_scroll(self, actual_ticks):
        if actual_ticks > self.ticks + (self.delay / self.level):
            self.ticks = actual_ticks
            return True
        return False