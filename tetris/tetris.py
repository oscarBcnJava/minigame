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
BACKGROUND_COLOR = (225, 240, 229)
GRID_COLOR = (0, 0, 0)
T_COLOR = (160,0,240)
S_COLOR = (0,240,0)
Z_COLOR = (0, 255, 0)
L_COLOR = (240,160,0)
J_COLOR = (0,0,240)
O_COLOR = (240,240,0)
I_COLOR = (0,240,240)

COLORS = [BACKGROUND_COLOR, T_COLOR, S_COLOR, Z_COLOR, L_COLOR, J_COLOR, O_COLOR, I_COLOR]

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
    global line_sound
    global four_lines_sound
    line_sound = pygame.mixer.Sound('tetris/sounds/laser.wav')
    four_lines_sound = pygame.mixer.Sound('tetris/sounds/laser_4_in_1.wav')

    pygame.freetype.init()
    score_font = pygame.freetype.Font(font_path, font_size)
    game_score = Score(0, 0)
    pygame.init()
   
    screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
    background_image = pygame.image.load("tetris/images/background-2.jpg").convert()
    background_image = pygame.transform.smoothscale(background_image, screen.get_size())

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
            delete_filled_lines(board, game_score)
            actual_piece = next_piece
            next_piece = Piece(3, 0)

        # TODO Check this. Using 1 for now
        # level = len([fila for fila in board if 0 not in fila]) // 10 + 1
        level = 1
        if level > MAX_LEVEL:
            level = MAX_LEVEL
        speed = START_SPEED + level * INCREMENT_SPEED

        screen.fill(BACKGROUND_COLOR)
        screen.blit(background_image, dest = (0, 0 , 1, 1))
        draw_board(board, screen)
        draw_piece(actual_piece, screen, actual_piece.x, actual_piece.y)
        

        draw_piece(next_piece, screen, 12, 2)

        if (not isMovementPossible(actual_piece, board, 0, 0)):
            pygame.quit()
            quit()
        score(screen, score_font, game_score.score)

        pygame.display.flip()

        clock.tick(speed)


def score(screen, font, score):
    font.render_to(screen, (100, 2), "Score: " + str(score), GRID_COLOR, None, size=64)

def create_board():
    board = [[0 for _ in range(10)] for _ in range(20)]
    return board

def draw_rect(x, y, color, screen, border):
    pygame.draw.rect(screen, color, (300 + x * 40, (y * 40) + 120, 40, 40))
    pygame.draw.rect(screen, GRID_COLOR, (300 + x * 40,  (y * 40) + 120, 40, 40), border)

def draw_board(board, screen):
    for row in range(len(board) - 1):
        for column in range(len(board[row])):
            color = COLORS[board[row][column]]
            border = 1
            if color == BACKGROUND_COLOR: border = -1
            draw_rect(column, row, color, screen, border)

def draw_piece(piece, screen, x, y):
    color = COLORS[piece.index + 1]
    for row in range(len(piece.type)):
        for column in range(len(piece.type[row])):
            if piece.type[row][column] != 0:
                draw_rect(x + column, y + row, color, screen, 1)

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

def draw_next_piece(piece, screen):
    draw_rect(12, 2, COLORS[piece.index + 1], screen, 1)

def add_piece_to_board(piece, board):
    for row in range(0, len(piece.type)):
        for column in range(0, len(piece.type[row])):
            if piece.type[row][column] != 0:
                board[piece.y + row][piece.x + column] = piece.index + 1

def delete_filled_lines(board, score):
    filled_lines = []
    
    for row in range(len(board) - 1, 0, -1):
        row_items_not_zero = 0
        row_length = len(board[row])
        for column in range(row_length):
            if board[row][column] != 0:
                row_items_not_zero += 1
                if row_items_not_zero == row_length:
                    filled_lines.append(row);

    lines_deleted = 0
    for filled in filled_lines:
        lines_deleted += 1
        board.pop(filled)
        score.increase_score(lines_deleted)
        line_sound.play()  
    
    if (len(filled_lines) == 4):
        four_lines_sound.play()
        score.increase_score(4)

    for filled in filled_lines:
        board.insert(0, [0]* row_length)

if __name__ == "__main__":
    main()
