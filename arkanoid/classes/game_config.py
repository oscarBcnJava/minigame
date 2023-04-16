import pygame.display
import os
from pygame.rect import Rect
from util.vector2D import Vec2d



class GameConfig():
    SCREEN_WIDTH = 900
    SCREEN_HEIGHT = 700
    WALL_ROWS = 20
    WALL_COLUMNS = 20
    WALL_WIDTH = 32
    BACKGROUND_COLOR = (0,0,0)
    FPS = 60

    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), 0, self.WALL_WIDTH)
        # self.brick_wall_hit_image = pygame.image.load(self.getResource(["images", "sprites", "brick_tile.png"])).convert_alpha()
        # self.brick_wall_hit_image = pygame.image.load(self.getResource(["images", "sprites", "brick_tile_hit.png"])).convert_alpha()
        # self.hit_wall = pygame.mixer.Sound(self.getResource(["sounds","pickupCoin.wav"]))
        # self.stick_image = pygame.image.load(self.getResource(["images", "sprites", "stick_128_32.png"])).convert_alpha()
    
    def get_screen_limits_rect(self) -> Rect:
        return Rect(self.WALL_WIDTH, self.WALL_WIDTH, (self.WALL_COLUMNS * self.WALL_WIDTH) - (2 * self.WALL_WIDTH), (self.WALL_ROWS * self.WALL_WIDTH) - (2 * self.WALL_WIDTH)) 

    def get_ball_config(self):
        return {'init_position': Vec2d(390.0,490.0), 'init_direction': Vec2d(0,1), 'speed': 5}

    def get_stick_config(self):
        return {'init_position': Vec2d(188.0,580.0), 'init_direction': Vec2d(1.0,0.0), 'speed': 5}
    
    # def getResource(self, path_elements):
    #     print(os.path.realpath("."))
    #     return os.path.join(os.path.dirname(os.path.realpath(__file__)),*path_elements)



        
        
    

