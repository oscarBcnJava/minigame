import pygame, sys, os, math
from pygame.math import Vector2 as Vec2d
pygame.init()

screen = pygame.display.set_mode((800, 800))

def main():
    num_points = 0
    points = []
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.circle(screen,pygame.color.THECOLORS["yellow"],(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]),10)
                points.append(pygame.mouse.get_pos())
                num_points += 1

        if num_points == 2:
            pygame.draw.line(screen, pygame.color.THECOLORS["red"], points[0], points[1], 2)
            vector = Vec2d(points[0][0] - points[1][0], points[1][0] - points[1][1])
            # print(vector.angle)
            vector.reflect(Vec2d(1,1))
            # radians = math.radians(90)
            # print(math.cos())
            # print(vector)
            pygame.draw.line(screen, pygame.color.THECOLORS["red"], points[1], (vector.x, vector.y), 2)
        if (num_points == 3):
            num_points = 0
            points.clear()
            screen.fill(pygame.color.THECOLORS["black"])
        pygame.display.flip()

def quit():
    print("Quit game")
    sys.exit()

def getResource(path_elements):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)),*path_elements)

if __name__ == "__main__":
    main()
