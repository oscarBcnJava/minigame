from pygame.sprite import Sprite
import pygame
from util.vector2D import Vec2d
from typing import Tuple
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
        self.rect = self.update_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def get_displacement(self):
        return Vec2d(    
        self.direction.x * self.speed,
        self.direction.y * self.speed)
    
    def update_rect(self): 
        self.rect = self.image.get_rect().move(
            self.pos.x - self.image_w / 2, 
            self.pos.y - self.image_h / 2)
    
    def move(self, horizontal_limits):
        displacement = self.get_displacement()
        self.pos += displacement

        if self.pos.x - (self.image_w/2) <= horizontal_limits[0]:
                self.pos.x = horizontal_limits[0] + (self.image_w/2) + 1
                self.direction.x = 0
        elif self.pos.x + (self.image_w/2) >= horizontal_limits[1]:
                self.pos.x = horizontal_limits[1] - (self.image_w/2) - 1
                self.direction.x = 0

        self.update_rect()

    def blit(self):
        self.screen.blit(self.image, self.rect)

    # returns range -1, 1 depending if collision is on the left or on the right. 0 should be on the middle
    def get_collision_factor(self, collision_point: Tuple[int, int]):
        if collision_point == None: return 0

        collision_point_x = collision_point[0]
        collision_point_x = -(self.image_w/2) + collision_point_x
        factor = collision_point_x  / (self.image_w / 2)

        if factor >= 1:
            return 1
        elif factor <= -1:
            return -1
        else: return factor


    

