import os, sys
import pygame
from arkanoid.classes.ball import Ball
from arkanoid.classes.wall import Wall
from arkanoid.classes.stick import Stick
from arkanoid.classes.level import Level
from arkanoid.classes.game_config import GameConfig
from pygame.sprite import Group
from pytmx.util_pygame import load_pygame

def start():
    global hit_wall, brick_wall_image, brick_wall_hit_image, sprite_group, ball, gc

    clock = pygame.time.Clock()
    pygame.init()
    gc = GameConfig()
    screen = gc.screen
    
    brick_wall_image = pygame.image.load(getResource(["images", "sprites", "brick_tile.png"])).convert_alpha()
    brick_wall_hit_image = pygame.image.load(getResource(["images", "sprites", "brick_tile_hit.png"])).convert_alpha()
    hit_wall = pygame.mixer.Sound(getResource(["sounds","pickupCoin.wav"]))
    stick_image = pygame.image.load(getResource(["images", "sprites", "stick_128_32.png"])).convert_alpha()
    ball_image = pygame.image.load(getResource(["images", "Balls", "Shiny", "Ball.png"])).convert_alpha()
    level = load_pygame(getResource(["images", "maps", "level.tmx"]))
    ball = Ball(ball_image, gc)
    stick = Stick(stick_image, gc)
    level = Level(screen, level)
    sprite_group = Group()

    add_walls_to_group()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    stick.direction.x = -1.0
                if event.key == pygame.K_RIGHT:
                    stick.direction.x = 1.0
                if event.key == pygame.K_UP:
                    stick.direction.x = 0.0

            if event.type == pygame.QUIT:
                quit()

        screen.fill(gc.BACKGROUND_COLOR)

        draw_wall(screen)
    
        ball.move(level=level)
        stick.move()
        level.blit()
        check_ball_stick_collision(ball, stick, screen)
        # if level.check_collision(ball):
        #     ball.handle_collision()

        pygame.display.flip()
        clock.tick(gc.FPS) 

def add_walls_to_group():
    for y in range(gc.WALL_ROWS):
        for x in range(gc.WALL_COLUMNS):
            if (y == 0 or y == gc.WALL_ROWS - 1 or x == 0 or x == gc.WALL_COLUMNS - 1):
                horizontal = False
                if x == 0 or x == gc.WALL_COLUMNS -1:
                    horizontal = True
                wall = Wall(brick_wall_image, brick_wall_hit_image, (x * gc.WALL_WIDTH, y * gc.WALL_WIDTH), horizontal)
                sprite_group.add(wall)

def draw_wall(screen):
    sprite_group.draw(screen)

def check_wall_collision(ball):
    sprite_collided = pygame.sprite.spritecollideany(ball, sprite_group, pygame.sprite.collide_mask)
    if  sprite_collided != None and type(sprite_collided) == Wall:
        # sc_rect = sprite_collided.rect

        # line_left_sprite_collided = LineString([(sc_rect.topleft[0], sc_rect.topleft[1]), (sc_rect.bottomleft[0], sc_rect.bottomleft[1])])
        # line_right_sprite_collided = LineString([(sc_rect.topright[0], sc_rect.topright[1]), (sc_rect.bottomright[0], sc_rect.bottomright[1])])
        # line_top_sprite_collided = LineString([(sc_rect.topleft[0], sc_rect.topleft[1]), (sc_rect.topright[0], sc_rect.topright[1])])
        # line_bottom_sprite_collided = LineString([(sc_rect.bottomleft[0], sc_rect.bottomleft[1]), (sc_rect.bottomright[0], sc_rect.bottomright[1])])

        # print(line_left_sprite_collided)
        # # line_between_objects = LineString([(ball.prev_pos.x, ball.prev_pos.y), (sc_rect.centerx, sc_rect.centery)])
        # # 
        # # print(f"center x: {sc_rect.centerx}, center y: {sc_rect.centery}")
        # ball.dir_points.append((sc_rect.centerx, sc_rect.centery))
        # line_between_objects = LineString(ball.dir_points)
        # # line_between_objects = LineString([(ball.dir_points[0][0], ball.dir_points[0][1]),(ball.dir_points[len(ball.dir_points) - 1][0], ball.dir_points[len(ball.dir_points) - 1][1]),(ball.pos.x, ball.pos.y), (sc_rect.centerx, sc_rect.centery)])
        # # line_between_objects = LineString(ball.dir_points)
        # print(f"line between objects: {line_between_objects}")
        # if line_left_sprite_collided.intersects(line_between_objects) or line_right_sprite_collided.intersects(line_between_objects):
        #     ball.handle_collision(horizontal_collision = True)
        #     sprite_collided.handle_collision()
        #     print("horizontal")
        # else:
        #     ball.handle_collision(horizontal_collision = False)
        #     sprite_collided.handle_collision()
        #     print("vertical")
        # # elif line_between_objects.intersects(line_top_sprite_collided) or line_between_objects.intersects(line_bottom_sprite_collided):
        # #     ball.handle_collision(horizontal_collision = False)
        # #     sprite_collided.handle_collision()
        # #     print("vertical")
        offset = (ball.rect.x - sprite_collided.rect.x), (ball.rect.y - sprite_collided.rect.y)
        # col_position = sprite_collided.mask.overlap_mask(ball.mask, (0,0))
        # print(f"collision {col_position}")

        horizontal = True
        if ball.mask.overlap(sprite_collided.topMask, offset) or ball.mask.overlap(sprite_collided.bottomMask, offset):
            horizontal = False
        elif ball.mask.overlap(sprite_collided.leftMask, offset) or ball.mask.overlap(sprite_collided.rightMask, offset):
            horizontal = True
            
                                                      
        print(f"left {ball.mask.overlap(sprite_collided.leftMask, offset)}")
        print(f"right {ball.mask.overlap(sprite_collided.rightMask, offset)}")
        print(f"top {ball.mask.overlap(sprite_collided.topMask, offset)}")
        print(f"down {ball.mask.overlap(sprite_collided.bottomMask, offset)}")
        
        
        ball.handle_collision(horizontal_collision = horizontal)
        return [None , sprite_collided.horizontal]
    return None

def check_ball_stick_collision(ball, stick, screen):
    if pygame.sprite.collide_mask(ball, stick):
        collision_factor = stick.get_collision_factor(pygame.sprite.collide_mask(stick, ball))
        ball.handle_collision(hit_factor = collision_factor)

def quit():
    print("Quit game")
    sys.exit()

def getResource(path_elements):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)),*path_elements)
