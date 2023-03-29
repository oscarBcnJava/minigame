import pygame
import random

# Screen config
WIDTH_SCREEN = 600
HEIGHT_SCREEN = 800

# Code colors RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)

COLORS = [WHITE, BLACK, RED, GREEN, BLUE, YELLOW, MAGENTA, CYAN]

# Piece types 
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

# game config
FPS = 60
START_LEVEL = 1
MAX_LEVEL = 100
START_SPEED = 10
INCREMENT_SPEED = 1

def main():
    print("Starting")
    pygame.init()
    screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
    pygame.display.set_caption('Tetris')

    # TODO update music
    pygame.mixer.music.load('resources/soundtrack.mp3') 
    pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()
    actual_piece = Piece(3, 0)
    next_piece = Piece(3, 0)
    board = create_board()
    level = START_LEVEL
    speed = START_SPEED

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    actual_piece.move_left()
                    if colision(actual_piece, board):
                        actual_piece.move_right()
                if event.key == pygame.K_RIGHT:
                    actual_piece.move_right()
                    if colision(actual_piece, board):
                        actual_piece.move_left()
                if event.key == pygame.K_DOWN:
                    actual_piece.move_down()
                    if colision(actual_piece, board):
                        actual_piece.move_up()
                if event.key == pygame.K_UP:
                    actual_piece.turn()
                    if colision(actual_piece, board):
                        actual_piece.turn_clockwise()


        actual_piece.move_down()
        print(actual_piece.y)
        if colision(actual_piece, board):
            actual_piece.move_up()
            
            # TODO add method
            add_piece_to_board(actual_piece, board)

            delete_lines(board)
            next_piece = Piece(3, 0)
            actual_piece = next_piece
            
            if colision(actual_piece, board):
                pygame.quit()
                quit()

        #TODO Check this. Using 1 for now
        # level = len([fila for fila in board if 0 not in fila]) // 10 + 1
        level = 1
        if level > MAX_LEVEL:
            level = MAX_LEVEL
        speed = START_SPEED + level * INCREMENT_SPEED

        screen.fill(WHITE)
        draw_board(board, screen)
        draw_piece(actual_piece, screen)
        pygame.display.update()

        clock.tick(speed)


class Piece:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.choice(PIECES)
        self.rotation = 0

    def turn(self):
        self.rotation = (self.rotation + 1) % len(self.tipo)

    def turn_clockwise(self):
        self.rotation = (self.rotation - 1) % len(self.tipo)

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

    def move_up(self):
        self.y -= 1
    
    def move_down(self):
        self.y += 1


def create_board():
    board = [[0 for _ in range(10)] for _ in range(20)]
    board += [[1 for _ in range(10)]]
    return board


def draw_rect(x, y, color, pantalla):
    pygame.draw.rect(pantalla, color, (x * 30, y * 30, 30, 30))
    pygame.draw.rect(pantalla, BLACK, (x * 30, y * 30, 30, 30), 1)


def draw_board(board, screen):
    for row in range(len(board) - 1):
        for column in range(len(board[row])):
            color = COLORS[board[row][column]]
            draw_rect(column, row, color, screen)


def draw_piece(piece, screen):
    color = COLORS[PIECES.index(piece.type)]
    for row in range(len(piece.type)):
        for column in range(len(piece.type[row])):
            if piece.type[row][column] != 0:
                draw_rect(piece.x + column, piece.y + row, color, screen)


def colision(piece, board):
    for row in range(len(piece.type)):
        for column in range(len(piece.type[row])):
            if piece.type[row][column] != 0:
                x = piece.x + column
                y = piece.y + row
                if x < 0 or x >= 10 or y >= 20 or board[y][x] != 0:
                    print("colision")
                    return True

def add_piece_to_board(piece, board):
    for row in range(len(piece.type)):
        for column in range(len(piece.type[row])):
            if piece.type[row][column] != 0:
                board[piece.y + row][piece.x + column] = PIECES.index(piece.type)


    # TODO            
def delete_lines(board):
    # missing implementation

    print("missing implementation")


if __name__ == "__main__":
    main()
