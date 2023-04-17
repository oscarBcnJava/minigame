from pygame.sprite import Sprite
import pygame
from util.vector2D import Vec2d
from typing import Tuple
class Stick(Sprite):
    
    def __init__(self, image, game_config):
        super().__init__()
        self.stick_config = game_config.get_stick_config()
        self.gc = game_config
        self.screen = self.gc.screen
        self.image = image
        self.pos = self.stick_config["init_position"]
        self.prev_pos = self.pos
        self.direction = self.stick_config["init_direction"].normalized()
        self.speed = self.stick_config["speed"]
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
    
    def move(self):
        displacement = self.get_displacement()
        self.pos += displacement
        self.check_screen_limits()
        self.update_rect()
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
    
    def check_screen_limits(self):
        if self.pos.x - (self.image_w/2) <= self.gc.get_screen_limits_rect().left:
            self.pos.x = self.gc.get_screen_limits_rect().left + (self.image_w/2)
        elif self.pos.x + (self.image_w/2) >= self.gc.get_screen_limits_rect().right:
            self.pos.x = self.gc.get_screen_limits_rect().right - (self.image_w/2)
            
         


    

