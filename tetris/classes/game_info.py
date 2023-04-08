REMAINING_LINES = {1: 10, 2: 12, 3: 15, 4: 20, 5: 30}

class GameInfo:
    def __init__(self, score, max_score, level):
        self.score = score
        self.max_score = max_score
        self.level = level
        self.remaining_lines = REMAINING_LINES[level]

    def increase_score(self, increment):
        self.score += 100 * increment
        if self.score > self.max_score:
            self.max_score = self.score