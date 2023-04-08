from pygame.sprite import Sprite
from util.vector2D import Vec2d
import pygame

class Ball(Sprite):
    def __init__(self, screen, image, init_position, init_direction, speed):
        super().__init__()
        self.screen = screen
        self.image = image
        self.pos = Vec2d(init_position)
        self.prev_pos = Vec2d(self.pos)
        self.direction = Vec2d(init_direction).normalized()
        self.init_direction = init_direction
        self.speed = speed
        self.image_w, self.image_h = self.image.get_size()
        self.rect = image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
    
    def move(self):
        displacement = Vec2d(    
            self.direction.x * self.speed,
            self.direction.y * self.speed)

        self.prev_pos = Vec2d(self.pos)
        self.pos += displacement
        self.update_rect()
    
    def reset_move(self):
        self.pos = Vec2d(self.prev_pos)
        self.update_rect()
        
    def update_rect(self):
        self.rect = self.image.get_rect().move(
            self.pos.x - self.image_w / 2, 
            self.pos.y - self.image_h / 2)
        
    def blit(self):
        self.screen.blit(self.image, self.rect)

    def boing(self, horizontal_hit = False, hit_percentage = 0):
        if horizontal_hit == True:
            self.direction.y = -self.direction.y
        else:
            self.direction.x = -self.direction.x
                            # self.direction.rotate(-1 * self.direction.get_angle())
   

