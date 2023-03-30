import random


PIECES = [
    [[1, 1, 1],
     [0, 1, 0]],  # T
    [[0, 2, 2],
     [2, 2, 0]],  # S
    [[3, 3, 0],
     [0, 3, 3]],  # Z
    [[4, 0, 0],
     [4, 4, 4]],  # L
    [[0, 0, 5],
     [5, 5, 5]],  # J
    [[6, 6],
     [6, 6]],  # O
    [[0, 7, 0, 0],
     [0, 7, 0, 0],
     [0, 7, 0, 0],
     [0, 7, 0, 0]]  # I
]

class Piece:
    def __init__(self, x, y):
        pieceRandomIndex = random.randint(0, len(PIECES) - 1)
        self.x = x
        self.y = y
        self.index = pieceRandomIndex
        self.type = PIECES[pieceRandomIndex]
        self.rotation = 1

    def turn(self):
        self.type = list(zip(*self.type[::-1]))

    def turn_clockwise(self):
        self.type = list(zip(*self.type))[::-1]

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

    def move_up(self):
        self.y -= 1
    
    def move_down(self):
        self.y += 1