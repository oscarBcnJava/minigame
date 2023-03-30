class Score:
    def __init__(self, score, max_score):
        self.score = score
        self.max_score = max_score

    def increase_score(self):
        self.score += 100