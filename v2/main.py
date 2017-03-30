import pygame
from Utils import *
import MainMenu

STATE = 'menu'
RUNNING = True
SCREEN = None
RESOLUTION = None

def main():
    read_settings()
    build_window()
    loop()


def build_window():
    global RESOLUTION, SCREEN
    # Create the game screen
    SCREEN = pygame.display.set_mode(RESOLUTION)
    # Set window info
    pygame.display.set_icon(SCREEN)
    pygame.display.set_caption('Solaris')
    pygame.display.flip()
    # Make the background of the game
    BACKGROUND = pygame.Surface(SCREEN.get_size())
    BACKGROUND.fill((0, 0, 0))


def read_settings():
    settings_file = None
    try:
        settings_file = open('config.txt', 'r')
    except:
        make_settings()
        settings_file = open('config.txt', 'r')
    lines = settings_file.readlines()
    for line in lines:
        if line.startswith('resolution'):
            global RESOLUTION
            fields = line.strip().split()
            RESOLUTION = (int(fields[1]), int(fields[2]))


def make_settings():
    settings_file = open('config.txt', 'w')
    contents = 'resolution 800 600'
    settings_file.writelines(contents)


def loop():
    while RUNNING is True:
        window_event_handler()
        if STATE == 'menu':
            MainMenu.render()


def window_event_handler():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global RUNNING
            RUNNING = False
            return

if __name__ == '__main__':
    main()