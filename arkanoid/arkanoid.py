import os, sys
import pygame
from arkanoid.classes.ball import Ball
from arkanoid.classes.wall import Wall
from arkanoid.classes.stick import Stick
from pygame.sprite import Group
from math import atan2, degrees
from shapely.geometry import LineString

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
WALL_ROWS = 20
WALL_COLUMNS = 20
BACKGROUND_COLOR = (0,0,0)
FPS = 60

def start():
    global hit_wall, brick_wall_image, brick_wall_hit_image, sprite_group, ball

    clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

    ball_image = pygame.image.load(getResource(["images", "sprites", "arkanoid_ball_color.png"])).convert_alpha()
    brick_wall_image = pygame.image.load(getResource(["images", "sprites", "brick_tile.png"])).convert_alpha()
    brick_wall_hit_image = pygame.image.load(getResource(["images", "sprites", "brick_tile_hit.png"])).convert_alpha()
    hit_wall = pygame.mixer.Sound(getResource(["sounds","pickupCoin.wav"]))
    stick_image = pygame.image.load(getResource(["images", "sprites", "stick_128_32.png"])).convert_alpha()
    ball = Ball(screen, ball_image, init_position=(190.0,490.0), init_direction=(1,0.5), speed=10)
    stick = Stick(screen, stick_image, init_position=(188.0,580.0), init_direction=(1.0,0.0), speed=5)
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

        screen.fill(BACKGROUND_COLOR)

        draw_wall(screen)
        check_wall_collision(ball)
        ball.move()
        stick.move((31, (32 * (WALL_COLUMNS - 1))))
        
        pygame.display.flip()
        check_ball_stick_collision(ball, stick, screen)
        clock.tick(60) 

def add_walls_to_group():
    for y in range(WALL_ROWS):
        for x in range(WALL_COLUMNS):
            if (y == 0 or y == WALL_ROWS - 1 or x == 0 or x == WALL_COLUMNS - 1):
                horizontal = False
                if x == 0 or x == WALL_COLUMNS -1:
                    horizontal = True
                wall = Wall(brick_wall_image, brick_wall_hit_image, (x * 32, y * 32), horizontal)
                sprite_group.add(wall)

def draw_wall(screen):
    sprite_group.draw(screen)

def check_wall_collision(ball):
    sprite_collided = pygame.sprite.spritecollideany(ball, sprite_group, pygame.sprite.collide_mask)
    if  sprite_collided != None:
        sc_rect = sprite_collided.rect

        line_left_sprite_collided = LineString([(sc_rect.topleft[0], sc_rect.topleft[1]), (sc_rect.bottomleft[0], sc_rect.bottomleft[1])])
        line_right_sprite_collided = LineString([(sc_rect.topright[0], sc_rect.topright[1]), (sc_rect.bottomright[0], sc_rect.bottomright[1])])
        line_top_sprite_collided = LineString([(sc_rect.topleft[0], sc_rect.topleft[1]), (sc_rect.topright[0], sc_rect.topright[1])])
        line_bottom_sprite_collided = LineString([(sc_rect.bottomleft[0], sc_rect.bottomleft[1]), (sc_rect.bottomright[0], sc_rect.bottomright[1])])

        line_between_objects = LineString([(ball.prev_pos.x, ball.prev_pos.y), (sc_rect.centerx, sc_rect.centery)])

        if line_left_sprite_collided.intersects(line_between_objects) or line_right_sprite_collided.intersects(line_between_objects):
            ball.handle_collision(horizontal_collision = True)
        elif line_between_objects.intersects(line_top_sprite_collided) or line_between_objects.intersects(line_bottom_sprite_collided):
            ball.handle_collision(horizontal_collision = False)

        sprite_collided.handle_collision()

    return False

def check_ball_stick_collision(ball, stick, screen):
    
    if pygame.sprite.collide_mask(ball, stick):
        collision_factor = stick.get_collision_factor(pygame.sprite.collide_mask(stick, ball))
        ball.handle_collision(hit_factor = collision_factor)

def quit():
    print("Quit game")
    sys.exit()

def getResource(path_elements):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)),*path_elements)

if __name__ == "__main__":
    main()