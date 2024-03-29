from pygame.sprite import Sprite
from util.vector2D import Vec2d
import pygame

class Ball(Sprite):
    def __init__(self, image, game_config):
        super().__init__()
        self.gc = game_config
        self.ball_config = self.gc.get_ball_config()
        self.screen = self.gc.screen
        self.image = pygame.transform.scale(image, (16, 16))
        self.pos = self.ball_config["init_position"]
        self.prev_pos = self.pos
        self.direction = self.ball_config["init_direction"].normalized()
        self.speed = self.ball_config["speed"]
        self.image_w, self.image_h = self.image.get_size()
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)
        
    def move(self, level, position = None, horizontal = False):
        horizontalTemp = False
        collision_groups = level.get_bricks_group()
        if position == None:
            displacement = Vec2d(
                self.direction.x * self.speed,
                self.direction.y)
            self.prev_pos = Vec2d(self.pos)
            self.pos += displacement
            self.update_rect()
            if pygame.sprite.spritecollide(self, collision_groups, False): 
                horizontalTemp = True

            displacement = Vec2d(    
                self.direction.x,
                self.direction.y * self.speed)
            self.prev_pos = Vec2d(self.pos)
            self.pos += displacement
            self.update_rect()
            brick_list = pygame.sprite.spritecollide(self, collision_groups, False)
            if brick_list: 
                self.handle_collision(horizontal_collision=horizontalTemp)
                level.handle_collision(brick_list)
        else: 
            self.pos.x = position[0]
            self.pos.y = position[1]

        self.update_rect()
        self.check_screen_limits()
        
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
                if self.direction.x == 0 and hit_factor != 0:
                    self.direction.x = hit_factor
                else:
                    self.direction.x *= (hit_factor * 1.2)
                    if self.direction.x < 0 and hit_factor > 0: self.direction.x *= -1
                    elif self.direction.x > 0 and hit_factor < 0: self.direction.x *= -1
                    if self.direction.x < 0 and self.direction.x > -0.6: self.direction.x = -0.6
                    elif self.direction.x > 0 and self.direction.x < 0.6: self.direction.x = 0.6
        else:
            self.direction.x = -self.direction.x
    
    def check_screen_limits(self):
        rect_margin = self.gc.get_screen_limits_rect()

        if self.pos.x <= rect_margin.left:
            self.pos.x = rect_margin.left
            self.handle_collision(horizontal_collision=True)
        elif self.pos.x >= rect_margin.right:
            self.pos.x = rect_margin.right
            self.handle_collision(horizontal_collision=True)
        elif self.pos.y <= rect_margin.top:
            self.pos.y = rect_margin.top
            self.handle_collision()
        elif self.pos.y >= rect_margin.bottom:
            self.pos.y = rect_margin.bottom
            self.handle_collision()

