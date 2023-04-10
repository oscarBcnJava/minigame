from pygame.sprite import Sprite
from util.vector2D import Vec2d
import pygame

class Ball(Sprite):
    def __init__(self, screen, image, init_position, init_direction, speed):
        super().__init__()
        self.screen = screen
        self.image = pygame.Surface((21,21))
        self.pos = Vec2d(init_position)
        self.prev_pos = Vec2d(self.pos)
        self.direction = Vec2d(init_direction).normalized()
        self.init_direction = init_direction
        self.speed = speed
        self.image_w, self.image_h = self.image.get_size()
        self.image.fill(pygame.color.THECOLORS["white"])
        self.image.set_colorkey(pygame.color.THECOLORS["white"])
        pygame.draw.circle(self.image, pygame.color.THECOLORS["yellow"], center = (10,10), radius = 5)
        self.rect = image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)
        
    def move(self):
        displacement = Vec2d(    
            self.direction.x * self.speed,
            self.direction.y * self.speed)

        self.prev_pos = Vec2d(self.pos)
        self.pos += displacement
        self.update_rect()
        self.screen.blit(self.image, self.rect)

    def reset_move(self):
        self.pos = Vec2d(self.prev_pos)
        self.update_rect()
        
    def update_rect(self):
        self.rect = self.image.get_rect().move(
            self.pos.x - self.image_w / 2, 
            self.pos.y - self.image_h / 2)

    def handle_collision(self, horizontal_collision = False, hit_factor = 0.0):
        if horizontal_collision == False:
            self.direction.y = -self.direction.y
            if (hit_factor != 0):
                self.direction.x *= (hit_factor * 1.5)
                if self.direction.x < 0 and hit_factor > 0: self.direction.x *= -1
                elif self.direction.x > 0 and hit_factor < 0: self.direction.x *= -1
                if self.direction.x < 0 and self.direction.x > -0.6: self.direction.x = -0.6
                elif self.direction.x > 0 and self.direction.x < 0.6: self.direction.x = 0.6
        else:
            self.direction.x = -self.direction.x   

