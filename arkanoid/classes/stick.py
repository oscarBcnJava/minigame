from pygame.sprite import Sprite
import pygame
from util.vector2D import Vec2d

class Stick(Sprite):
    
    def __init__(self, screen, image, init_position, init_direction, speed):
        super().__init__()
        self.screen = screen
        self.image = image
        self.pos = Vec2d(init_position)
        self.prev_pos = Vec2d(self.pos)
        self.direction = Vec2d(init_direction).normalized()
        self.speed = speed
        self.image_w, self.image_h = self.image.get_size()
        self.rect = image.get_rect().move(self.pos.x, self.pos.y)
        self.mask = pygame.mask.from_surface(self.image)

    def blit(self):
        displacement = Vec2d(    
        self.direction.x * self.speed,
        self.direction.y * self.speed)

        self.prev_pos = Vec2d(self.pos)
        self.pos += displacement

        self.rect = self.image.get_rect().move(
            self.pos.x - self.image_w / 2, 
            self.pos.y - self.image_h / 2)
        
        self.screen.blit(self.image, self.rect)

