from pygame.sprite import Sprite
import pygame
from util.vector2D import Vec2d
from typing import Tuple

class Brick(Sprite):
    
    def __init__(self, image, pos, breakable, live: int):
        super().__init__()
        self.image = image
        self.pos = pos
        self.breakable = breakable
        self.live = live
        self.actual_lives = live
        self.image_w, self.image_h = self.image.get_size()
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.mask = pygame.mask.from_surface(self.image)
    
    def hit(self):
        if self.breakable:
            self.actual_lives -= 1


    


    

