import pygame

MENU_TEXT = None
BACKGROUND = None
INIT = False

# TODO: Figure out how to get global vars from main or if this needs to be static


def init():
    # Get globals from main
    global SCREEN, RESOLUTION

    # Make background sheet
    global BACKGROUND
    BACKGROUND = pygame.Surface(RESOLUTION)
    BACKGROUND.fill(0, 0, 0)

    # Make text modules
    pygame.font.init()
    global MENU_TEXT
    MENU_TEXT = pygame.font.SysFont('Arial', 30)


def render():
    global INIT
    if INIT is False:
        init()
        INIT = True
    SCREEN.blit(BACKGROUND)
    SCREEN.blit(MENU_TEXT.render('Something', False, (255, 255, 255)), (0, 0))
