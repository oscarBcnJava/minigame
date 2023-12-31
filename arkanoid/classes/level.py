from pygame.sprite import Sprite
from util.vector2D import Vec2d
from arkanoid.classes.brick import Brick
from pygame.sprite import Group
import pygame

class Level():
    def __init__(self, screen, level):
        super().__init__()
        self.screen = screen
        self.tiled_map = level
        self.bricks_group = Group()
        self.remaining_bricks = 0
        self.add_bricks_to_group()
    
    def add_bricks_to_group(self):
        for x, y, image in self.tiled_map.get_layer_by_name("bricks").tiles():
            breakable = self.tiled_map.get_tile_properties(x, y, 0).get('breakable')
            life = self.tiled_map.get_tile_properties(x, y, 0).get('live')
            if breakable:
                self.remaining_bricks += 1
            brick = Brick(image, (x * 32, y * 32), breakable, life)
            self.bricks_group.add(brick)

    def blit(self):
        self.bricks_group.draw(self.screen)

    def handle_collision(self, brick_list):
        for brick in brick_list:
            brick.hit()
            if brick.actual_lives <= 0:
                self.bricks_group.remove(brick)
    
    def get_bricks_group(self):
        return self.bricks_group
    

    
        
        
    

