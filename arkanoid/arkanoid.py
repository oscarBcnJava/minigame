import os, sys
import pygame
from arkanoid.classes.ball import Ball
from arkanoid.classes.wall import Wall
from arkanoid.classes.stick import Stick
from util.vector2D import Vec2d
from pygame.rect import Rect
from pygame.sprite import Group

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
WALL_ROWS = 20
WALL_COLUMNS = 20
BACKGROUND_COLOR = (225, 240, 229)
FPS = 60

def start():
    global hit_wall, brick_wall_image, brick_wall_hit_image, sprite_group
    clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

    ball_image = pygame.image.load(getResource(["images", "sprites", "arkanoid_ball_color.png"])).convert_alpha()
    brick_wall_image = pygame.image.load(getResource(["images", "sprites", "brick_tile.png"])).convert_alpha()
    brick_wall_hit_image = pygame.image.load(getResource(["images", "sprites", "brick_tile_hit.png"])).convert_alpha()
    hit_wall = pygame.mixer.Sound(getResource(["sounds","pickupCoin.wav"]))
    stick_image = pygame.image.load(getResource(["images", "sprites", "stick.png"])).convert_alpha()

    # ball = Ball(screen, ball_image, init_position=(190,190), init_direction=(1, 0.5), speed=8)
    ball = Ball(screen, ball_image, init_position=(190,190), init_direction=(1, 0.5), speed=12)
    stick = Stick(screen, stick_image, init_position=(100,580), init_direction=(0,0), speed=0.5)
    sprite_group = Group()
    sprite_group.add(stick)
    add_walls_to_group()

    while True:
        x = 0
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    stick.direction.x = -1
                    # ball.pos.x -= 10
                if event.key == pygame.K_RIGHT:
                    # ball.pos.x += 10
                    stick.direction.x = 1
                if event.key == pygame.K_UP:
                    # stick.direction.x = -1
                    ball.pos.y -= 7
                if event.key == pygame.K_DOWN:
                    ball.pos.y += 7
                if event.key == pygame.K_l:
                    ball.pos.y += 1
            if event.type == pygame.QUIT:
                quit()

        screen.fill(BACKGROUND_COLOR)

        draw_wall(screen, brick_wall_image)
        check_wall_collision_with(ball)
        ball.move()
       
            
        

        ball.blit()
        stick.blit()
        pygame.display.flip()
        
        # check_wall_collision_with(stick)
        # check_ball_stick_collision(ball, stick, screen)
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

def draw_wall(screen, image):
    sprite_group.draw(screen)

def check_wall_collision_with(obj):
    sprite_collided = pygame.sprite.spritecollideany(obj, sprite_group, pygame.sprite.collide_mask)
    if  sprite_collided != None:
        if type(obj) == Ball:
            print(sprite_collided)
            obj.boing(horizontal_hit = not sprite_collided.horizontal)
            sprite_collided.boing()
            # hit_wall.play()
        elif type(obj) == Stick:
            obj.direction.x = 0
        return True

def check_ball_stick_collision(ball, stick, screen):
    
    if pygame.sprite.collide_rect(ball, stick):
        clip = stick.rect.clip(ball.rect)
        print(clip)
        pygame.draw.rect(screen, pygame.Color('red'), clip)
    else:
        print("no coll")
            

def quit():
    print("Quit game")
    sys.exit()

def getResource(path_elements):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)),*path_elements)

if __name__ == "__main__":
    main()