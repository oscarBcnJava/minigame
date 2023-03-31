import pygame
import sys
import os
import pygame.freetype
from tetris.classes.piece import Piece
from tetris.classes.score import Score

# Screen config
WIDTH_SCREEN = 1200
HEIGHT_SCREEN = 1600

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

# game config
FPS = 60
START_LEVEL = 1
MAX_LEVEL = 100
START_SPEED = 4
INCREMENT_SPEED = 1


def start(): 
    main()

def main():
    font_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"fonts","Marlboro.ttf")
    font_size = 5
    pygame.mixer.init()
    line_sound = pygame.mixer.Sound('tetris/sounds/laser.wav')
    pygame.freetype.init()
    score_font = pygame.freetype.Font(font_path, font_size)
    game_score = Score(0, 0)
    pygame.init()
   

    screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
    pygame.display.set_caption('Tetris')

    pygame.mixer.music.load('tetris/sounds/level3.mp3')
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
                    if (isMovementPossible(actual_piece, board, -1, 0)):
                        actual_piece.move_left()
                if event.key == pygame.K_RIGHT:
                    if (isMovementPossible(actual_piece, board, 1, 0)):
                        actual_piece.move_right()
                if event.key == pygame.K_DOWN:
                    if (isMovementPossible(actual_piece, board, 0, 1)):
                        actual_piece.move_down()
                if event.key == pygame.K_SPACE:
                    if isMovementPossible(actual_piece, board, 0, 0, True):
                        actual_piece.turn()

        if isMovementPossible(actual_piece, board, 0, 1):
            actual_piece.move_down()
        else:
            add_piece_to_board(actual_piece, board)
            delete_filled_lines(board, game_score, line_sound)
            next_piece = Piece(3, 0)
            actual_piece = next_piece

        # TODO Check this. Using 1 for now
        # level = len([fila for fila in board if 0 not in fila]) // 10 + 1
        level = 1
        if level > MAX_LEVEL:
            level = MAX_LEVEL
        speed = START_SPEED + level * INCREMENT_SPEED

        screen.fill(WHITE)
        draw_board(board, screen)
        draw_piece(actual_piece, screen)
        if (not isMovementPossible(actual_piece, board, 0, 0)):
            pygame.quit()
            quit()
        score(screen, score_font, game_score.score)
        pygame.display.update()

        clock.tick(speed)


def score(screen, font, score):
    font.render_to(screen, (100, 2), "Score: " + str(score), BLACK, None, size=64)

def create_board():
    board = [[0 for _ in range(10)] for _ in range(20)]
    return board


def draw_rect(x, y, color, screen):
    pygame.draw.rect(screen, color, (x * 40, (y * 40) + 120, 40, 40))
    pygame.draw.rect(screen, BLACK, (x * 40,  (y * 40) + 120, 40, 40), 1)


def draw_board(board, screen):
    for row in range(len(board) - 1):
        for column in range(len(board[row])):
            color = COLORS[board[row][column]]
            draw_rect(column, row, color, screen)


def draw_piece(piece, screen):
    color = COLORS[piece.index + 1]
    for row in range(len(piece.type)):
        for column in range(len(piece.type[row])):
            if piece.type[row][column] != 0:
                draw_rect(piece.x + column, piece.y + row, color, screen)


def isMovementPossible(piece, board, nextX, nextY, rotate=False):
    pieceType = piece.type
    if (rotate):
        pieceType = list(zip(*pieceType[::-1]))
    for row in range(len(pieceType)):
        for column in range(len(pieceType[row])):
            if pieceType[row][column] != 0:
                x = piece.x + column + nextX
                y = piece.y + row + nextY
                if x < 0 or x >= 10 or y >= 19 or board[y][x] != 0:
                    return False
    return True


def colision(piece, board):
    for row in range(len(piece.type)):
        for column in range(len(piece.type[row])):
            if piece.type[row][column] != 0:
                x = piece.x + column
                y = piece.y + row
                if x < 0 or x >= 10 or y >= 20 or board[y][x] != 0:
                    return True


def add_piece_to_board(piece, board):
    for row in range(0, len(piece.type)):
        for column in range(0, len(piece.type[row])):
            if piece.type[row][column] != 0:
                board[piece.y + row][piece.x + column] = piece.index + 1


def delete_filled_lines(board, score, sound):
    lines_deleted = 0
    for row in range(len(board) - 1, 0, -1):
        row_items_not_zero = 0
        row_length = len(board[row])
        for column in range(row_length):
            if board[row][column] != 0:
                row_items_not_zero += 1
                if row_items_not_zero == row_length:
                    board.pop(row)
                    board.insert(0, [0]* row_length)
                    lines_deleted += 1
                    score.increase_score()
                    sound.play()    
if __name__ == "__main__":
    main()
