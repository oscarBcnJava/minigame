import pygame
import pygame_menu
from pygame_menu.examples import create_example_window
from tetris.tetris import start

WINDOW_SIZE = (640, 480)

def main() -> None:
    global surface
    clock = pygame.time.Clock()

    surface = create_example_window("-- MiniGame --", WINDOW_SIZE)
    
    play_menu = pygame_menu.Menu(height=WINDOW_SIZE[1] * 0.7,
                                 title = "MiniGame",
                                 width=WINDOW_SIZE[0] * 0.75)
    
    play_menu.add.button("Tetris", start)
    play_menu.add.button("Quit", pygame_menu.events.EXIT)

    while True:
        clock.tick(60)

        
        play_menu.mainloop(surface, background, disable_loop=True, fps_limit=60)
        pygame.display.flip()
        
def background(): 
    surface.fill((128, 0, 128))


if __name__ == '__main__':
    main()