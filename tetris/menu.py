import pygame_menu
from pygame_menu.examples import create_example_window
from tetris import 
from typing import Tuple, Any

surface = create_example_window('TeTrIs', (600, 400))


def set_difficulty(selected: Tuple, value: Any) -> None:
    print(f'Set difficulty to {selected[0]} ({value})')


def start_the_game() -> None:
    global user_name
    tetris.main()


menu = pygame_menu.Menu(
    height=300,
    theme=pygame_menu.themes.THEME_BLUE,
    title='Welcome',
    width=400
)

user_name = menu.add.text_input('Name: ', default='John Doe', maxchar=10)
menu.add.selector('Difficulty: ', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

if __name__ == '__main__':
    menu.mainloop(surface)