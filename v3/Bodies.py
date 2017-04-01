import pygame
import math
from random import randint
import Utils


class Body:
    def __init__(self, radius, color, action_listener=None, gravity=1, has_player_gravity=False, parent=None, orbit_radius=0, pos=None, is_player=False, counter=0):
        self.pos = pos
        if pos is None:
            self.pos = [0, 0]
        self.radius = radius
        self.color = color
        self.has_gravity = has_player_gravity
        self.gravity = gravity
        self.parent = parent
        self.orbit_radius = orbit_radius
        self.counter = counter
        self.children = []
        self.is_player = is_player
        self.action_listener = action_listener

    def update(self, player):

        if self.is_player is True:
            self.action_listener.run('camerafollow', [self.pos])

        # Run child code
        for child in self.children:
            child.update(player)

        # Interact with player
        if player is not None:

            if self.action_listener is not None and self.hit_detect(player.pos) is True and player.interaction_timeout == 0:
                self.is_player = True
                self.action_listener.run('deleteplayer')

            if self.has_gravity is True:
                self.apply_gravity(player)

        # Orbit parent
        if self.parent is not None:
            self.counter += self.parent.gravity/(self.orbit_radius**2)
            xoffset = self.orbit_radius * math.cos(self.counter)
            yoffset = -self.orbit_radius * math.sin(self.counter)
            self.pos = [self.parent.pos[0] + xoffset, self.parent.pos[1] + yoffset]

        if self.is_player is True:
            self.action_listener.run('launchplayer', [self])

    def hit_detect(self, obj_pos):
        dist_x = abs(self.pos[0] - obj_pos[0])
        dist_y = abs(self.pos[1] - obj_pos[1])
        linear_dist = math.sqrt(dist_x ** 2 + dist_y ** 2)
        if linear_dist <= self.radius:
            return True

    def apply_gravity(self, player):
        if player.interaction_timeout > 0:
            return
        dist_x = abs(self.pos[0] - player.pos[0])
        dist_y = abs(self.pos[1] - player.pos[1])
        linear_dist = math.sqrt(dist_x ** 2 + dist_y ** 2)
        if linear_dist == 0:
            linear_dist = 1
        dist_x_normalized = dist_x / linear_dist
        dist_y_normalized = dist_y / linear_dist
        grav_force = self.gravity * (1 / (linear_dist**2))
        x_grav_force = grav_force * dist_x_normalized
        y_grav_force = grav_force * dist_y_normalized
        if player.pos[0] > self.pos[0]:
            x_grav_force = x_grav_force * -1
        if player.pos[1] > self.pos[1]:
            y_grav_force = y_grav_force * -1
        player.vel[0] += x_grav_force
        player.vel[1] += y_grav_force

    def render(self, screen, camera_pos):
        # Draw orbit path
        if self.parent is not None and self.orbit_radius > 0:
            parent_pos = [round(self.parent.pos[0] - camera_pos[0]), round(self.parent.pos[1] - camera_pos[1])]
            pygame.draw.circle(screen, (100, 100, 100), parent_pos, self.orbit_radius, 1)

        # Draw body
        pos = [round(self.pos[0] - camera_pos[0]), round(self.pos[1] - camera_pos[1])]
        pygame.draw.circle(screen, self.color, pos, self.radius)

        # Render children
        for child in self.children:
            child.render(screen, camera_pos)

        if self.is_player is True:
            mouse_pos = pygame.mouse.get_pos()
            pygame.draw.line(screen, (255, 100, 100), pos, mouse_pos, 1)


class Player:
    def __init__(self, pos, color, radius, vel, action_listener):
        self.pos = pos
        self.color = color
        self.radius = radius
        if vel is None:
            vel = [0, 0]
        self.vel = vel
        self.speed = 0.01
        self.trail = []
        self.action_listener = action_listener
        self.interaction_timeout = 200

    def update(self):
        if self.interaction_timeout > 0:
            self.interaction_timeout -= 1

        self.action_listener.run('camerafollow', [self.pos])

        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        self.make_trail()
        if len(self.trail) > 1000:
            self.trail.pop(0)

    def render(self, screen, camera_pos):
        color = self.color
        if self.interaction_timeout > 0:
            color = (255, 255, 255)

        for body in self.trail:
            body.render(screen, camera_pos)

        pos = [round(self.pos[0] - camera_pos[0]), round(self.pos[1] - camera_pos[1])]
        pygame.draw.circle(screen, color, pos, self.radius)

    def make_trail(self):
        pos = [self.pos[0], self.pos[1]]
        self.trail.append(Body(0, (100, 100, 100), None, 0, False, None, 0, pos))


def next_pos(pos, vel):
    # predict trajectory of bodies
    pos[0] += vel[0]
    pos[1] += vel[1]
    
    
def generate_system(pos, action_listener):
    # Make star
    star_size = randint(30, 100)
    star = Body(star_size, random_color(), action_listener, star_size * 10, True, None, 0, pos)

    # Make planets
    num_planets = randint(3, 10)
    for i in range(1, num_planets):
        planet_size = randint(5, 20)
        new_planet = Body(planet_size, random_color(), action_listener, planet_size * 8, True, star, i * randint(200, 400), None, False, randint(0, 100))
        star.children.append(new_planet)

        # Make Moons
        num_moons = randint(0, 5)
        for j in range(1, num_moons):
            moon_size = randint(2, 5)
            new_moon = Body(moon_size, random_color(), action_listener, 1, False, new_planet, j * randint(20, 30), None, False, randint(0, 100))
            new_planet.children.append(new_moon)

    return star
    
    
def random_color():
    color = (randint(0, 255), randint(0, 255), randint(0, 255))
    return color
