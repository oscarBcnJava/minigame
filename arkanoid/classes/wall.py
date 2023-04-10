from pygame.sprite import Sprite
import pygame
from threading import Timer
from util.vector2D import Vec2d

class Wall(Sprite):
    balls_hit = []
    
    def __init__(self, image, image_hit, init_position, horizontal):
        super().__init__()
        self.image_no_hit = image
        self.image_hit = image_hit
        self.image = self.image_no_hit
        self.horizontal = horizontal
        self.pos = Vec2d(init_position)
        self.prev_pos = Vec2d(self.pos)
        self.image_w, self.image_h = self.image.get_size()
        self.rect = image.get_rect().move(self.pos.x, self.pos.y)
        self.mask = pygame.mask.from_surface(self.image)
        self.timer = Timer(2, self.clear_balls_hit)

    def handle_collision(self):
        self.image = self.image_hit
        Wall.balls_hit.append(self)
        self.timer = Timer(0.1, self.clear_balls_hit)
        self.timer.start()

    def clear_balls_hit(self):
        for wall in Wall.balls_hit:
            wall.image = self.image_no_hit
            Wall.balls_hit.clear
            self.timer.cancel()

