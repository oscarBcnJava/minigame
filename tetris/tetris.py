import pygame
import sys
import os
import pygame.freetype
from tetris.classes.piece import Piece
from tetris.classes.game_info import GameInfo
from tetris.classes.scroll import Scroll

# Screen config
WIDTH_SCREEN = 1200
HEIGHT_SCREEN = 1600
OFFSET_GAMEBOARD_LEFT = 400
OFFSET_GAMEBOARD_TOP = 150

# Code colors RGB
BACKGROUND_COLOR = pygame.color.THECOLORS['gray69']
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

def start(): 
    main()

def main():
    
    font_path = getResource(["fonts","OldTimer.ttf"])
    pygame.mixer.init()
    global line_sound
    global four_lines_sound
    line_sound = pygame.mixer.Sound(getResource(["sounds","laser.wav"]))
    four_lines_sound = pygame.mixer.Sound(getResource(["sounds","laser_4_in_1.wav"]))
    hit_floor_sound = pygame.mixer.Sound(getResource(["sounds","hit_floor.wav"]))

    pygame.freetype.init()
    score_font = pygame.freetype.Font(font_path, 1)
    game_info = GameInfo(0, 0, 1)
    pygame.init()
   
    screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
    background_image = pygame.image.load(getResource(["images","background-2.jpg"])).convert()
    background_image = pygame.transform.smoothscale(background_image, screen.get_size())

    pygame.display.set_caption('Tetris')

    pygame.mixer.music.load(getResource(["sounds","level3.mp3"]))
    pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()

    actual_piece = Piece(3, 0)
    next_piece = Piece(3, 0)
    board = create_board()
    auto_down = False
    piece_sound_should_play = False

    scroll = Scroll(START_LEVEL, pygame.time.get_ticks())
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
                if event.key == pygame.K_LEFT:
                    if (isMovementPossible(actual_piece, board, -1, 0)):
                        actual_piece.move_left()
                if event.key == pygame.K_RIGHT:
                    if (isMovementPossible(actual_piece, board, 1, 0)):
                        actual_piece.move_right()
                if event.key == pygame.K_DOWN:
                    if (isMovementPossible(actual_piece, board, 0, 1)):
                        auto_down = True
                        actual_piece.move_down()
                if event.key == pygame.K_SPACE:
                    if isMovementPossible(actual_piece, board, 0, 0, True):
                        actual_piece.turn()

            if event.type == pygame.KEYUP:
                auto_down = False

        next_movement_possible = isMovementPossible(actual_piece, board, 0, 1)
        if not next_movement_possible and not piece_sound_should_play:
            print("sound")
            piece_sound_should_play = True
            hit_floor_sound.play()

        if scroll.is_allowed_scroll(pygame.time.get_ticks(), auto_down):
            if next_movement_possible:
                actual_piece.move_down()
            else:
                add_piece_to_board(actual_piece, board, hit_floor_sound)
                delete_filled_lines(board, game_info)
                actual_piece = next_piece
                next_piece = Piece(3, 0)
                piece_sound_should_play = False

        screen.fill(BACKGROUND_COLOR)
        screen.blit(background_image, dest = (0, 0 , 1, 1))
        draw_game_board(board, screen)
        draw_info_boards(screen, score_font, game_info)
        draw_piece(actual_piece, screen, actual_piece.x, actual_piece.y)
        

        draw_piece(next_piece, screen, 12, 2)

        if (not isMovementPossible(actual_piece, board, 0, 0)):
            pygame.quit()
            quit()

        pygame.display.flip()
        clock.tick(FPS)  

def create_board():
    board = [[0 for _ in range(10)] for _ in range(20)]
    return board

def draw_rect(x, y, color, screen, border):
    pygame.draw.rect(screen, color, (OFFSET_GAMEBOARD_LEFT + x * 40, OFFSET_GAMEBOARD_TOP + (y * 40), 40, 40))
    pygame.draw.rect(screen, GRID_COLOR, (OFFSET_GAMEBOARD_LEFT + x * 40,  OFFSET_GAMEBOARD_TOP + (y * 40), 40, 40), border)

def draw_game_board(board, screen):
    for row in range(len(board) - 1):
        for column in range(len(board[row])):
            color = COLORS[board[row][column]]
            border = 1
            if color == BACKGROUND_COLOR: border = -1
            draw_rect(column, row, color, screen, border)

def draw_info_boards(screen, font, game_info):
    score_board = pygame.Rect(100,  150, 280, 210)
    next_piece_board = pygame.Rect(820,  150, 230, 260)
    screen.fill(pygame.color.THECOLORS['gray90'], score_board)
    screen.fill(pygame.color.THECOLORS['gray90'], next_piece_board)
    font.render_to(screen, (120, 180), "Level: " + str(game_info.level), GRID_COLOR, None, size=22)
    font.render_to(screen, (120, 220), "Score: " + str(game_info.score), GRID_COLOR, None, size=22)
    font.render_to(screen, (120, 260), "High-score: " + str(game_info.max_score), GRID_COLOR, None, size=22)
    font.render_to(screen, (120, 300), "Remaining lines: " + str(game_info.remaining_lines), GRID_COLOR, None, size=22)
    font.render_to(screen, (910, 180), "Next", GRID_COLOR, None, size=22)

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

def add_piece_to_board(piece, board, hit_floor_sound):
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
        score.decrease_remaining_lines()
        line_sound.play()  
    
    if (len(filled_lines) == 4):
        four_lines_sound.play()
        score.increase_score(4)

    for filled in filled_lines:
        board.insert(0, [0]* row_length)

def getResource(path_elements):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)),*path_elements)

if __name__ == "__main__":
    main()
