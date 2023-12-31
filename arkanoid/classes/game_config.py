import pygame.display
from pygame.rect import Rect
from util.vector2D import Vec2d


class GameConfig():
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 700
    WALL_ROWS = 20
    WALL_COLUMNS = 25
    WALL_WIDTH = 32
    BACKGROUND_COLOR = (0,0,0)
    FPS = 60

    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), 0, self.WALL_WIDTH)
        self.bricks_group = list()
    
    def get_screen_limits_rect(self) -> Rect:
        return Rect(self.WALL_WIDTH, self.WALL_WIDTH, (self.WALL_COLUMNS * self.WALL_WIDTH) - (2* self.WALL_WIDTH), (self.WALL_ROWS * self.WALL_WIDTH) - (2 * self.WALL_WIDTH)) 

    def get_ball_config(self):
        return {'init_position': Vec2d(390.0,490.0), 'init_direction': Vec2d(0,1), 'speed': 5}

    def get_stick_config(self):
        return {'init_position': Vec2d(188.0,580.0), 'init_direction': Vec2d(1.0,0.0), 'speed': 5}



        
        
    

