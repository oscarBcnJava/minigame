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
        self.subTop = pygame.Surface.subsurface(self.image, (0,0,32,2))
        self.subBottom = pygame.Surface.subsurface(self.image, (0,29,32,2))
        self.mask = pygame.mask.from_surface(self.image)
        self.subLeft = pygame.Surface.subsurface(self.image, (0,3,2,28))
        self.subRight = pygame.Surface.subsurface(self.image, (30,3,2,28))
        self.topMask = pygame.mask.from_surface(self.subTop)
        self.bottomMask = pygame.mask.from_surface(self.subBottom)
        self.leftMask = pygame.mask.from_surface(self.subLeft)
        self.rightMask = pygame.mask.from_surface(self.subRight)
        
        self.timer = Timer(2, self.clear_balls_hit)
        olistTop = self.topMask.outline()
        olistBottom = self.bottomMask.outline()
        olistLeft = self.leftMask.outline()
        olistRight = self.rightMask.outline()
        pygame.draw.lines(self.subTop,(200,150,150),1,olistTop)
        pygame.draw.lines(self.subBottom,(200,150,150),2,olistBottom)
        pygame.draw.lines(self.subLeft,(200,150,150),2,olistLeft)
        pygame.draw.lines(self.subRight,(200,150,150),2,olistRight)

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

