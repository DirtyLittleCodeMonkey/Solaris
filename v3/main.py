import pygame
import math
import settings
import Menu


running = True
screen = None
fonts = []
current_menu = None
display_menu = True


def main():
    init()
    loop()


def init():
    global screen, fonts
    resx, resy = settings.get_resolution()
    # Create the game screen
    screen = pygame.display.set_mode((resx, resy))
    # Set window info
    pygame.display.set_icon(screen)
    pygame.display.set_caption('Solaris')
    # Generate fonts
    pygame.font.init()
    for i in range(0, 10):
        fonts.append(pygame.font.SysFont('Arial', i*10))


def loop():
    while running is True:
        if display_menu is True:
            current_menu.render()
        else:
            update()
            render()


# Update game logic
def update():
    pass


# Draw elements to the screen
def render():
    pass



def window_event_handler():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global running
            running = False
            return


if __name__ == '__main__':
    main()