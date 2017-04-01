import pygame
import settings
import Menu
import Bodies
import HUD
import Utils

running = True
screen = None

fonts = []
current_menu = None
display_menu = True
current_hud = None
action_listener = None
resolution = None
key_limiter = False

testbody = None
player = None
camera_pos = [0, 0]
launch = False


def main():
    init()
    loop()


def init():
    global screen, fonts, resolution
    resx, resy = settings.get_resolution()
    resolution = [resx, resy]
    # Create the game screen
    screen = pygame.display.set_mode(resolution)
    # Set window info
    pygame.display.set_icon(screen)
    pygame.display.set_caption('Solaris')
    # Generate fonts
    pygame.font.init()
    for i in range(0, 10):
        fonts.append(pygame.font.SysFont('Arial', i*10))
    # Make the main menu
    global action_listener
    action_listener = ActionListener()
    global current_menu
    current_menu = Menu.main_menu(fonts, resolution, action_listener)

    global testbody
    testbody = Bodies.generate_system([0, 0], action_listener)

    global player
    player = Bodies.Player([500, 500], (255, 100, 100), 3, [0, 0], action_listener)

    global current_hud
    current_hud = HUD.test_hud(fonts, resolution, action_listener, testbody)


def loop():
    game_clock = pygame.time.Clock()
    while running is True:
        game_clock.tick(60)
        window_event_handler()
        if display_menu is True:
            current_menu.render(screen)
            pygame.display.flip()
        else:
            update()
            render()


# Update game logic
def update():
    key_listener()
    global testbody, player
    testbody.update(player)
    if player is not None:
        player.update()


# Draw elements to the screen
def render():

    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    testbody.render(screen, camera_pos)
    if player is not None:
        player.render(screen, camera_pos)

    current_hud.render(screen)

    pygame.display.flip()


# Listen for key presses during the game
def key_listener():
    global key_limiter, display_menu, current_menu
    keys_down = pygame.key.get_pressed()
    all_inactive = True
    for key in keys_down:
        if key == 1:
            all_inactive = False
            break
    if all_inactive is True:
        key_limiter = False

    # Pause the game
    if keys_down[pygame.K_ESCAPE] == 1:
        if key_limiter is False:
            key_limiter = True
            action_listener.run('pause')

    # Control the player
    global player
    if player is not None:
        if keys_down[pygame.K_UP] == 1:
            player.vel[1] -= player.speed
        if keys_down[pygame.K_DOWN] == 1:
            player.vel[1] += player.speed
        if keys_down[pygame.K_LEFT] == 1:
            player.vel[0] -= player.speed
        if keys_down[pygame.K_RIGHT] == 1:
            player.vel[0] += player.speed

    # Launch the player
    if player is None:
        global launch
        if keys_down[pygame.K_SPACE] == 1:
            launch = True
        else:
            launch = False


# Allows objects outside this module to run commands
class ActionListener:
    def __init__(self):
        self.command = ''

    def run(self, command, params=None):
        global current_menu, display_menu, running, player, testbody, camera_pos, current_hud, launch
        if command == 'play':
            display_menu = False
        elif command == 'quit':
            running = False
        elif command == 'options':
            current_menu = Menu.options_menu(fonts, resolution, action_listener)
        elif command == 'mainmenu':
            current_menu = Menu.main_menu(fonts, resolution, action_listener)
        elif command == 'resolution':
            current_menu = Menu.resolution_menu(fonts, resolution, action_listener)
        elif command == 'changeres':
            param = params[0]
            settings.set_resolution(param)
            current_menu = Menu.confirm_res_change(fonts, resolution, action_listener)
        elif command == 'pause':
            display_menu = True
            current_menu = Menu.pause_menu(fonts, resolution, action_listener)
        elif command == 'deleteplayer':
            player = None
        elif command == 'spawnplayer':
            player = Bodies.Player(params[0], params[1], params[2], params[3])
        elif command == 'gensystem':
            testbody = Bodies.generate_system([0,0], action_listener)
            player = Bodies.Player([500, 500], (255, 100, 100), 3, [0, 0], action_listener)
            current_hud = HUD.test_hud(fonts, resolution, action_listener, testbody)
            display_menu = False
        elif command == 'camerafollow':
            camera_pos = params[0]
            camera_pos = [camera_pos[0] - resolution[0]/2, camera_pos[1] - resolution[1]/2]
        elif command == 'launchplayer':
            if launch is True:
                planet = params[0]
                mouse_pos = pygame.mouse.get_pos()
                pos = [planet.pos[0], planet.pos[1]]
                vel = [(camera_pos[0] + mouse_pos[0])/100, (camera_pos[1] + mouse_pos[1])/100]
                player = Bodies.Player(pos, (255, 100, 100), 3, vel, action_listener)
                planet.is_player = False
                launch = False


def window_event_handler():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global running
            running = False
            return





if __name__ == '__main__':
    main()
