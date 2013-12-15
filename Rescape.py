#
# Pocket Universe: Rescape
# v1.55
# A game written in Python for CodeSkulptor.
# By Chloe Unrau 2013
# _____________________________________________________________________________
# _____________________________________________________________________________
# _____________________________________________________________________________


#
# READ ME
# _____________________________________________________________________________
# _____________________________________________________________________________
# _____________________________________________________________________________


"""

IMPORTANT: This game only works properly in the GOOGLE CHROME web browser.
This is due to different levels of compatibility of browsers with 
CodeSkulptor. If Chrome cannot load the file, try loading it in Chrome's
Incognito mode.

To play this game, copy & paste this code into CodeSkulptor.org, using
Google Chrome, and click the RUN button.

"""


#
# IMPORT MODULES
# _____________________________________________________________________________
# _____________________________________________________________________________
# _____________________________________________________________________________


import simplegui
import math
import random


#
# DEFINE GLOBAL VARIABLES
# _____________________________________________________________________________
# _____________________________________________________________________________
# _____________________________________________________________________________


# canvas
WIDTH = 800
HEIGHT = 600
CENTRE = [WIDTH / 2, HEIGHT / 2]
CTRL_WIDTH = 100

# control
total_score = 0
story_board = 0
game_is_paused = False
first_time = True
at_level_status = False
in_play = False
time = 0.5
levels_remaining = 10
anomoly_mass = 0
rescued_this_turn = False
beat_the_game = False
num_dimensions = {}
num_dimensions['x'] = 0
num_dimensions['y'] = 0

# game
default_friction = 0.02
friction = default_friction
default_hull_integrity = 5
hull_integrity = default_hull_integrity
safe_spawn_distance = 200
game_level = 0
disruptor_speed = 12
disruptor_lifespan = 10
disruptor_max = 3
teleporter_speed = 4
teleporter_lifespan = 20
teleporter_max = 1
ship_acceleration = 0.2
ship_turn_vel = 0.1
max_asteroids = 5
max_asteroid_speed = 30

# sprites
all_rocks = set([])
all_disruptors = set([])
all_explosions = set([])
all_teleporters = set([])
all_teleports = set([])
remove_rocks = set([])
remove_disruptors = set([])
remove_teleporters = set([])
remove_explosions = set([])
remove_teleports = set([])

# timers
rock_spawner_frequency = 1000
main_eh_frequency = 60
music_frequency = 9953
victory_frequency = 14765

# user interface
name_font = "monospace"
name_size = 14
name_colour = "#ffffff"
ui_font = "monospace"
ui_size = 12
ui_colour = "#ffffff"
ui_level_colour = "#73badb"
status_font = "monospace"
status_size = 24
status_colour = "#ffffff"
map_pos = [20, 51]


#
# DEFINE HELPER FUNCTIONS
# _____________________________________________________________________________
# _____________________________________________________________________________
# _____________________________________________________________________________


def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]


def dist(p, q):
    """ Return the distance in pixels between two objects. """
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


def randrange_nozero(a, b):
    """ Return as random.randrange[a, b) without returning 0. """
    _num = 0
    if not (a == 0 and b == 0):
        while _num == 0:
            _num = random.randrange(a, b)
    return _num


def asteroid_collision(source):
    """ Create a asteroid collision animation. """
    explosion = Sprite(
        'explosion', 
        asteroid_crash_image, 
        asteroid_crash_info, 
        source.get_pos(), 
        source.get_vel(), 
        source.get_angle(), 
        source.get_angle_vel(), 
        False, 
        damage_sound)
    all_explosions.add(explosion)


def debris_collision(source):
    """ Create a debris collision animation. """
    explosion = Sprite(
        'explosion', 
        debris_crash_image, 
        debris_crash_info, 
        source.get_pos(), 
        source.get_vel(), 
        source.get_angle(), 
        source.get_angle_vel(), 
        False, 
        damage_sound)
    all_explosions.add(explosion)


def asteroid_explosion(source):
    """ Create a asteroid explosion animation. """
    explosion = Sprite(
        'explosion', 
        asteroid_explosion_image, 
        asteroid_explosion_info, 
        source.get_pos(), 
        source.get_vel(), 
        source.get_angle(), 
        source.get_angle_vel(), 
        False, 
        explosion_sound)
    all_explosions.add(explosion)


def debris_explosion(source):
    """ Create a power-up and debris explosion animation. """
    explosion = Sprite(
        'explosion', 
        debris_explosion_image, 
        debris_explosion_info, 
        source.get_pos(), 
        source.get_vel(), 
        source.get_angle(), 
        source.get_angle_vel(), 
        False, 
        explosion_sound)
    all_explosions.add(explosion)
    powerup = Sprite(
        'powerup', 
        powerup_image, 
        powerup_info, 
        source.get_pos(), 
        source.get_vel(), 
        source.get_angle(), 
        source.get_angle_vel(), 
        False)
    all_rocks.add(powerup)


def lifeform_explosion(source):
    """ Create a lifeform explosion animation. """
    explosion = Sprite(
        'explosion', 
        lifeform_explosion_image, 
        lifeform_explosion_info, 
        source.get_pos(), 
        source.get_vel(), 
        source.get_angle(), 
        source.get_angle_vel(), 
        False, 
        explosion_sound)
    all_explosions.add(explosion)


def asteroid_teleport(source):
    """ Create an asteroid teleport animation. """
    teleport = Sprite(
        'teleport', 
        asteroid_teleport_image, 
        asteroid_teleport_info, 
        source.get_pos(), 
        source.get_vel(), 
        source.get_angle(), 
        source.get_angle_vel(), 
        False, 
        teleport_sound)
    all_teleports.add(teleport)


def debris_teleport(source):
    """ Create a debris teleport animation. """
    teleport = Sprite(
        'teleport', 
        debris_teleport_image, 
        debris_teleport_info, 
        source.get_pos(), 
        source.get_vel(), 
        source.get_angle(), 
        source.get_angle_vel(), 
        False, 
        teleport_sound)
    all_teleports.add(teleport)


def lifeform_teleport(source):
    """ Create a lifeform teleport animation. """
    teleport = Sprite(
        'teleport', 
        lifeform_teleport_image, 
        lifeform_teleport_info, 
        source.get_pos(), 
        source.get_vel(), 
        source.get_angle(), 
        source.get_angle_vel(), 
        False, 
        teleport_sound)
    all_teleports.add(teleport)


def clear_all_sprites(this_set):
    """ Remove all sprites in a given set. """
    remove_sprites = set([])
    for sprite in this_set:
        remove_sprites.add(sprite)
    this_set.difference_update(remove_sprites)


def clear_all_types():
    """ Remove all sprites from all sets. """
    clear_all_sprites(all_disruptors)
    clear_all_sprites(all_teleporters)
    clear_all_sprites(all_rocks)
    clear_all_sprites(all_explosions)
    clear_all_sprites(all_teleports)


def end_game(stop_play = True):
    """ Stop the game and reset variables. """
    global in_play, rescued_this_turn, friction
    my_ship.thrust = False
    my_ship.is_right = False
    my_ship.is_left = False
    friction = 0.1
    my_ship.angle_vel = 0
    rescued_this_turn = False
    my_map.found_mothership = False
    ship_thrust_sound.pause()
    ship_thrust_sound.rewind()
    clear_all_types()
    if stop_play:
        in_play = False


def game_over():
    """ Display the Game Over splash screen and reset variables. """
    global game_level, splash_image, game_is_paused, beat_the_game, total_score
    game_level = 0
    total_score = 0
    splash_image = splash_image_game_over
    game_is_paused = True
    beat_the_game = False
    die_sound.rewind()
    die_sound.play()
    game_over_sound.rewind()
    game_over_sound.play()


def new_game(dim, mass, play_now = True):
    """ Reset ship, mothership, variables, and create a new game and map. """
    global my_map, my_ship, mothership, in_play, friction, game_is_paused
    global anomoly_mass, splash_image, at_level_status, beat_the_game
    global hull_integrity

    if play_now:
        in_play = True
        beat_the_game = False
        game_is_paused = False
        at_level_status = False
        splash_image = splash_image_blank
        friction = default_friction
        if game_level == 1:
            hull_integrity = default_hull_integrity

    anomoly_mass = mass

    # num_dimensions x and y must both be even numbers with a maximum of 20
    num_dimensions['x'] = dim[0]
    num_dimensions['y'] = dim[1]

    # create a new map of the size of the current pocket universe
    my_map = Map(map_info, map_tile_info)

    # create a new mothership
    mothership = Sprite(
        'mothership', 
        mothership_low_image, 
        mothership_low_info, 
        [WIDTH / 2, HEIGHT / 2], 
        [0, 0], 
        0, 
        0.1, 
        True)

    # create a new ship
    my_ship = Sprite(
        'ship', 
        ship_image, 
        ship_info, 
        [WIDTH / 2, HEIGHT / 2], 
        [0, 0], 
        0, 
        0, 
        True)

    # ensure ship and mothership have different random dimensional coordinates
    mothership.relocate()
    my_ship.relocate()
    while my_ship.dim_coord == mothership.dim_coord:
        mothership.relocate()


def level_status():
    """ Display the Level Status screen. """
    global game_is_paused, at_level_status, levels_remaining
    global splash_image, beat_the_game, game_level
    end_game(False)
    game_is_paused = True
    levels_remaining = 10 - game_level
    if game_level < 10 and not beat_the_game:
        at_level_status = True
        splash_image = splash_image_level_status
        level_complete_sound.rewind()
        level_complete_sound.play()
    else:
        beat_the_game = True
        game_level = 0
        splash_image = splash_image_beat_game
        beat_game_sound.rewind()
        beat_game_sound.play()
        music_timer.stop()
        music.pause()
        victory_timer.start()
        victory_music.play()


def start_next_level():
    """ Prepare and start the next level. """
    global game_level, nebula_image, levels_remaining
    nebula_image = nebula_list[game_level]
    transmission_2.pause()
    game_level += 1
    if game_level == 1:
        levels_remaining = 10
    new_game([game_level*2, game_level*2], game_level*100)
    level_start_sound.rewind()
    level_start_sound.play()


def next_story_board():
    """ Display the next story board screen. """
    global first_time, story_board, story_image
    story_board += 1
    if story_board > 5:
        first_time = False
        start_next_level()
    else:
        if story_board == 1:
            transmission_1.rewind()
            transmission_1.play()
        else:
            transmission_1.pause()
            transmission_2.rewind()
            transmission_2.play()
        story_image = story_image_list[story_board]


def play_music():
    music.rewind()
    music.play()


def play_victory():
    victory_music.rewind()
    victory_music.play()


#
# DEFINE CLASSES
# _____________________________________________________________________________
# _____________________________________________________________________________
# _____________________________________________________________________________


class ImageInfo:
    def __init__(
        self, size, radius = 0, lifespan = None, animated = False):
        self.size = size
        self.centre = [self.size[0] / 2, self.size[1] / 2]
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_centre(self):
        return self.centre

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated


class Sprite:
    def __init__(self, kind, image, info, pos, vel, ang, 
        ang_vel = 0, lighting = False, sound = None):
        self.kind = str(kind)
        self.pos = list(pos)
        self.vel = list(vel)
        self.thrust = False
        self.is_right = False
        self.is_left = False
        self.at_mothership = False
        self.pos_changed = False
        self.angle = float(ang)
        self.angle_vel = float(ang_vel)
        self.forward_vel = list(angle_to_vector(self.get_angle()))
        self.image = image
        self.image_centre = list(info.get_centre())
        self.image_size = list(info.get_size())
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        self.life = 0
        self.dim_coord = [0, 0]
        self.score = 0
        self.life_forms = 0
        self.lighting = lighting
        if sound:
            sound.rewind()
            sound.play()

    def fire_missile(self, missile_kind):

        # calculate the position of the ship's nose
        nose_pos = [self.radius * math.cos(self.angle) + self.pos[0],
                    self.radius * math.sin(self.angle) + self.pos[1]]

        # fire a missile of a certain type

        if missile_kind == 'disruptor':

            # set missile velocity based on ship direction and velocity
            this_vel = [
                ((angle_to_vector(self.angle)[0] * disruptor_speed) 
                    + self.vel[0]), 
                ((angle_to_vector(self.angle)[1] * disruptor_speed) 
                    + self.vel[1])]

            # create a new disruptor missile
            if len(all_disruptors) < disruptor_max:
                disruptor = Sprite(
                    'disruptor', 
                    disruptor_image, 
                    disruptor_info, 
                    nose_pos, 
                    this_vel, 
                    my_ship.angle, 
                    0, 
                    False, 
                    disruptor_sound)
                # add new missile to the game
                all_disruptors.add(disruptor)
            else:
                # misfire if maximum disruptor shots are in play
                misfire_sound.rewind()
                misfire_sound.play()

        if missile_kind == 'teleporter':

            # set missile velocity based on ship direction and velocity
            this_vel = [
                ((angle_to_vector(self.angle)[0] * teleporter_speed) 
                    + self.vel[0]), 
                ((angle_to_vector(self.angle)[1] * teleporter_speed) 
                    + self.vel[1])]

            # create a new teleporter missile
            if len(all_teleporters) < teleporter_max:
                teleporter = Sprite(
                    'teleporter', 
                    teleporter_image, 
                    teleporter_info, 
                    nose_pos, 
                    this_vel, 
                    0, 
                    0.2, 
                    False,
                    teleporter_sound)
                # add new teleportens to the game
                all_teleporters.add(teleporter)
            else:
                # misfire if maximum teleporter shots are in play
                misfire_sound.rewind()
                misfire_sound.play()

    def get_pos(self):
        return self.pos

    def get_vel(self):
        return self.vel

    def get_angle(self):
        return self.angle

    def get_angle_vel(self):
        return self.angle_vel

    def get_dim_coord(self):
        return self.dim_coord

    def relocate(self, random_dim = True, x = 0, y = 0):
        """ Move this sprite to a random dimentional coordinate. """
        if random_dim:
            # relocate sprite to random dim-coords within current dimension
            x = random.randrange(0, num_dimensions['x'])
            y = random.randrange(0, num_dimensions['y'])
        self.dim_coord[0] = x
        self.dim_coord[1] = y
        my_map.update_tile(self.kind)
        self.update()

    def collide(self, this_sprite):
        """ Return true if this sprite collides with given sprite. """
        if dist(this_sprite.pos, self.pos) < this_sprite.radius + self.radius:
            return True

    def step_animate(self):
        """ Set the image of this sprite to the next animation frame. """
        self.image_centre[0] += self.image_size[0]
    
    def update(self):
        """ Update this sprite (called from the draw handler). """
        if self.kind == 'ship':

            # update directional velocity
            self.forward_vel = [angle_to_vector(self.angle)[0], 
                                angle_to_vector(self.angle)[1]]

            # update volocity as per thrust
            if self.thrust:
                self.vel[0] += self.forward_vel[0] * ship_acceleration
                self.vel[1] += self.forward_vel[1] * ship_acceleration

            # update velocity as per friction
            self.vel[0] *= (1 - friction)
            self.vel[1] *= (1 - friction)

        # update direction
        self.angle += self.angle_vel

        # update position
        self.pos[0] = (self.pos[0] + self.vel[0])
        self.pos[1] = (self.pos[1] + self.vel[1])

        # update dimensional coordinates
        if self.pos[0] < 0:
            self.dim_coord[0] -= 1
            self.dim_coord[0] %= num_dimensions['x']
            self.pos_changed = True
        if self.pos[0] > WIDTH:
            self.dim_coord[0] += 1
            self.dim_coord[0] %= num_dimensions['x']
            self.pos_changed = True
        if self.pos[1] < 0:
            self.dim_coord[1] -= 1
            self.dim_coord[1] %= num_dimensions['y']
            self.pos_changed = True
        if self.pos[1] > HEIGHT:
            self.dim_coord[1] += 1
            self.dim_coord[1] %= num_dimensions['y']
            self.pos_changed = True

        if self.pos_changed:
            my_map.update_tile(self.kind)
            self.pos_changed = False

        # wrap position
        self.pos[0] %= WIDTH
        self.pos[1] %= HEIGHT

    def draw(self, canvas):
        """ Draw this sprite. """
        canvas.draw_image(
            self.image, 
            self.image_centre, 
            self.image_size, 
            self.pos, 
            self.image_size,
            self.angle)
        if self.lighting:
            canvas.draw_image(
                lighting_image, 
                lighting_info.get_centre(), 
                lighting_info.get_size(), 
                self.pos, 
                self.image_size,
                0)


class Map:
    def __init__(self, info, tile_info):
        self.info = info
        self.tile_info = tile_info
        self.size = map_tile_info.get_size()[0] - 1
        self.found_mothership = False
        self.centre = [info.get_centre()[0] + 1, info.get_centre()[1] + 1]
        self.grid_size = [0, 0]
        self.grid_offset = -3
        self.mothership_pos = [0, 0]
        self.my_ship_pos = [0, 0]
        # set the size of the map based on num_dimensions + 1px to show border
        self.grid_size = [
            num_dimensions['x'] * map_tile_info.get_size()[0] + 1, 
            num_dimensions['y'] * map_tile_info.get_size()[1] + 1]
        # re-position the map based on the grid size (and magic numbers >_<)
        self.pos = list(map_pos)
        self.pos[0] += self.grid_size[0] / 2 + self.grid_offset
        self.pos[1] += self.grid_size[1] / 2 + self.grid_offset

    def update_tile(self, tile):
        """ Update the ship and mothership map markers. """
        if tile == 'mothership':
            self.mothership_pos[0] = map_pos[0] + (
                map_tile_info.get_size()[0] * mothership.dim_coord[0])
            self.mothership_pos[1] = map_pos[1] + (
                map_tile_info.get_size()[1] * mothership.dim_coord[1])
        if tile == 'ship':
            self.my_ship_pos[0] = map_pos[0] + (
                map_tile_info.get_size()[0] * my_ship.dim_coord[0])
            self.my_ship_pos[1] = map_pos[1] + (
                map_tile_info.get_size()[1] * my_ship.dim_coord[1])

    def draw(self, canvas):
        """ Draw this map. """

        # draw the map
        canvas.draw_image(
            map_image, 
            self.centre, 
            self.grid_size, 
            self.pos, 
            self.grid_size, 
            0)

        # draw the mothership tile
        if my_map.found_mothership:
            canvas.draw_image(
                map_tile_mothership, 
                map_tile_info.get_centre(), 
                map_tile_info.get_size(), 
                self.mothership_pos, 
                map_tile_info.get_size(), 
                0)

        #draw the ship tile
        canvas.draw_image(
            map_tile_ship, 
            map_tile_info.get_centre(), 
            map_tile_info.get_size(), 
            self.my_ship_pos, 
            map_tile_info.get_size(), 
            0)


#
# INITIALISE GRAPHICS & SOUNDS
# _____________________________________________________________________________
# _____________________________________________________________________________
# _____________________________________________________________________________


# All graphics are created by me for this game, and
# are copyright 2013 Chloe Unrau (www.chloeunrau.com)

splash_info = ImageInfo([800, 600])
splash_image_blank = simplegui.load_image("")
splash_image_game_over = simplegui.load_image(
    "http://www.chloeunrau.com/stuff/rescape/images/game-over.png")
splash_image_level_status = simplegui.load_image(
    "http://www.chloeunrau.com/stuff/rescape/images/level-status.png")
splash_image_beat_game = simplegui.load_image(
    "http://www.chloeunrau.com/stuff/rescape/images/beat-game.png")
splash_image = splash_image_blank

story_info = ImageInfo([800, 600])
story_image_0 = simplegui.load_image(
    "http://www.chloeunrau.com/stuff/rescape/images/splash.png")
story_image_1 = simplegui.load_image (
    "http://www.chloeunrau.com/stuff/rescape/images/story-1a.png")
story_image_2 = simplegui.load_image (
    "http://www.chloeunrau.com/stuff/rescape/images/story-2a.png")
story_image_3 = simplegui.load_image (
    "http://www.chloeunrau.com/stuff/rescape/images/story-3a.png")
story_image_4 = simplegui.load_image (
    "http://www.chloeunrau.com/stuff/rescape/images/story-4a.png")
story_image_5 = simplegui.load_image (
    "http://www.chloeunrau.com/stuff/rescape/images/story-5a.png")
story_image_list = [story_image_0, 
                    story_image_1, 
                    story_image_2, 
                    story_image_3, 
                    story_image_4, 
                    story_image_5]
story_image = story_image_list[0]

nebula_info = ImageInfo([800, 600])
nebula_0 = simplegui.load_image(
    "http://www.chloeunrau.com/stuff/rescape/images/nebula-0.jpg")
nebula_1 = simplegui.load_image(
    "http://www.chloeunrau.com/stuff/rescape/images/nebula-1.jpg")
nebula_2 = simplegui.load_image(
    "http://www.chloeunrau.com/stuff/rescape/images/nebula-2.jpg")
nebula_3 = simplegui.load_image(
    "http://www.chloeunrau.com/stuff/rescape/images/nebula-3.jpg")
nebula_4 = simplegui.load_image(
    "http://www.chloeunrau.com/stuff/rescape/images/nebula-4.jpg")
nebula_5 = simplegui.load_image(
    "http://www.chloeunrau.com/stuff/rescape/images/nebula-5.jpg")
nebula_6 = simplegui.load_image(
    "http://www.chloeunrau.com/stuff/rescape/images/nebula-6.jpg")
nebula_7 = simplegui.load_image(
    "http://www.chloeunrau.com/stuff/rescape/images/nebula-7.jpg")
nebula_8 = simplegui.load_image(
    "http://www.chloeunrau.com/stuff/rescape/images/nebula-8.jpg")
nebula_9 = simplegui.load_image(
    "http://www.chloeunrau.com/stuff/rescape/images/nebula-9.jpg")
nebula_list = [nebula_0, 
               nebula_1, 
               nebula_2, 
               nebula_3, 
               nebula_4, 
               nebula_5, 
               nebula_6, 
               nebula_7, 
               nebula_8, 
               nebula_9]
nebula_image = nebula_list[0]

grid_info = ImageInfo([631, 480])
grid_image = simplegui.load_image(
    "http://www.chloeunrau.com/stuff/rescape/images/grid.png")

interface_top_info = ImageInfo([800, 31])
interface_top_image = simplegui.load_image(
    "http://www.chloeunrau.com/stuff/rescape/images/interface-top.png")

interface_bottom_info = ImageInfo([800, 31])
interface_bottom_image = simplegui.load_image(
    "http://www.chloeunrau.com/stuff/rescape/images/interface-bottom.png")

lighting_info = ImageInfo([90, 90], 30)
lighting_image = simplegui.load_image(
    "http://www.chloeunrau.com/stuff/rescape/images/lighting.png")

ship_info = ImageInfo([90, 90], 30)
ship_image = simplegui.load_image(
    "http://www.chloeunrau.com/stuff/rescape/images/ship.png")

mothership_low_info = ImageInfo([154, 154], 77)
mothership_low_image = simplegui.load_image(
    "http://www.chloeunrau.com/stuff/rescape/images/mothership-low.png")

mothership_high_info = ImageInfo([800, 600])
mothership_high_image = simplegui.load_image(
    "http://www.chloeunrau.com/stuff/rescape/images/mothership-high.png")

disruptor_info = ImageInfo([10, 10], 3, disruptor_lifespan)
disruptor_image = simplegui.load_image(
    "http://www.chloeunrau.com/stuff/rescape/images/disruptor.png")

teleporter_info = ImageInfo([10, 10], 3, teleporter_lifespan)
teleporter_image = simplegui.load_image(
    "http://www.chloeunrau.com/stuff/rescape/images/teleporter.png")

map_info = ImageInfo([141, 141], 70)
map_image = simplegui.load_image(
    "http://www.chloeunrau.com/stuff/rescape/images/map.png")

map_tile_info = ImageInfo([7, 7])
map_tile_ship = simplegui.load_image(
    "http://www.chloeunrau.com/stuff/rescape/images/map-tile-ship.png")
map_tile_mothership = simplegui.load_image(
    "http://www.chloeunrau.com/stuff/rescape/images/map-tile-mothership.png")

asteroid_info = ImageInfo([81, 81], 40)
asteroid_image = simplegui.load_image(
    "http://www.chloeunrau.com/stuff/rescape/images/asteroid.png")

debris_info = ImageInfo([81, 81], 40)
debris_image = simplegui.load_image(
    "http://www.chloeunrau.com/stuff/rescape/images/debris.png")

lifeform_info = ImageInfo([81, 81], 30)
lifeform_image = simplegui.load_image(
    "http://www.chloeunrau.com/stuff/rescape/images/lifeform.png")

asteroid_crash_info = ImageInfo([128, 128], 64, 17, True)
asteroid_crash_image = simplegui.load_image(
    "http://www.chloeunrau.com/stuff/rescape/images/asteroid-collision.png")

debris_crash_info = ImageInfo([128, 128], 64, 17, True)
debris_crash_image = simplegui.load_image(
    "http://www.chloeunrau.com/stuff/rescape/images/debris-collision.png")

asteroid_explosion_info = ImageInfo([128, 128], 64, 17, True)
asteroid_explosion_image = simplegui.load_image(
    "http://www.chloeunrau.com/stuff/rescape/images/asteroid-explosion.png")

lifeform_explosion_info = ImageInfo([128, 128], 64, 17, True)
lifeform_explosion_image = simplegui.load_image(
    "http://www.chloeunrau.com/stuff/rescape/images/lifeform-explosion.png")

debris_explosion_info = ImageInfo([128, 128], 64, 17, True)
debris_explosion_image = simplegui.load_image(
    "http://www.chloeunrau.com/stuff/rescape/images/debris-explosion.png")

asteroid_teleport_info = ImageInfo([81, 81], 40.5, 24, True)
asteroid_teleport_image = simplegui.load_image(
    "http://www.chloeunrau.com/stuff/rescape/images/asteroid-teleport.png")

debris_teleport_info = ImageInfo([81, 81], 40.5, 24, True)
debris_teleport_image = simplegui.load_image(
    "http://www.chloeunrau.com/stuff/rescape/images/debris-teleport.png")

lifeform_teleport_info = ImageInfo([81, 81], 40.5, 24, True)
lifeform_teleport_image = simplegui.load_image(
    "http://www.chloeunrau.com/stuff/rescape/images/lifeform-teleport.png")

powerup_info = ImageInfo([32, 32], 16)
powerup_image = simplegui.load_image(
    "http://www.chloeunrau.com/stuff/rescape/images/power-up.png")


# royalty-free music from www.flashkit.com

music = simplegui.load_sound(
    "http://www.chloeunrau.com/stuff/rescape/sounds/music.mp3")
music.set_volume(1)

victory_music = simplegui.load_sound(
    "http://www.chloeunrau.com/stuff/rescape/sounds/music-2.mp3")
music.set_volume(1)


# royalty-free sound effects from www.freesound.org

disruptor_sound = simplegui.load_sound(
    "http://www.chloeunrau.com/stuff/rescape/sounds/disruptor-fire.mp3")
disruptor_sound.set_volume(0.8)

teleporter_sound = simplegui.load_sound(
    "http://www.chloeunrau.com/stuff/rescape/sounds/teleporter-fire.mp3")
teleporter_sound.set_volume(0.7)

misfire_sound = simplegui.load_sound(
    "http://www.chloeunrau.com/stuff/rescape/sounds/misfire.mp3")
misfire_sound.set_volume(0.5)

ship_thrust_sound = simplegui.load_sound(
    "http://www.chloeunrau.com/stuff/rescape/sounds/thruster.mp3")
ship_thrust_sound.set_volume(1)

explosion_sound = simplegui.load_sound(
    "http://www.chloeunrau.com/stuff/rescape/sounds/explosion-alt.mp3")
explosion_sound.set_volume(1)

teleport_sound = simplegui.load_sound(
    "http://www.chloeunrau.com/stuff/rescape/sounds/teleport.mp3")
teleport_sound.set_volume(1)

damage_sound = simplegui.load_sound(
    "http://www.chloeunrau.com/stuff/rescape/sounds/explosion.mp3")
damage_sound.set_volume(0.2)

lifeform_death_sound = simplegui.load_sound(
    "http://www.chloeunrau.com/stuff/rescape/sounds/life-forms-die.mp3")
lifeform_death_sound.set_volume(1)

powerup_sound = simplegui.load_sound(
    "http://www.chloeunrau.com/stuff/rescape/sounds/power-up.mp3")
powerup_sound.set_volume(0.3)

level_start_sound = simplegui.load_sound(
    "http://www.chloeunrau.com/stuff/rescape/sounds/level-start.mp3")
level_start_sound.set_volume(1)

level_complete_sound = simplegui.load_sound(
    "http://www.chloeunrau.com/stuff/rescape/sounds/level-complete.mp3")
level_complete_sound.set_volume(1)

beat_game_sound = simplegui.load_sound(
    "http://www.chloeunrau.com/stuff/rescape/sounds/level-complete.mp3")
beat_game_sound.set_volume(1)

score_sound = simplegui.load_sound(
    "http://www.chloeunrau.com/stuff/rescape/sounds/score-alt.mp3")
score_sound.set_volume(0.6)

die_sound = simplegui.load_sound(
    "http://www.chloeunrau.com/stuff/rescape/sounds/die.mp3")
die_sound.set_volume(1)

game_over_sound = simplegui.load_sound(
    "http://www.chloeunrau.com/stuff/rescape/sounds/game-over.mp3")
game_over_sound.set_volume(1)

transmission_1 = simplegui.load_sound(
    "http://www.chloeunrau.com/stuff/rescape/sounds/transmission-1.mp3")
transmission_1.set_volume(1)

transmission_2 = simplegui.load_sound(
    "http://www.chloeunrau.com/stuff/rescape/sounds/transmission-2.mp3")
transmission_2.set_volume(1)


#
# DEFINE EVENT HANDLERS
# _____________________________________________________________________________
# _____________________________________________________________________________
# _____________________________________________________________________________


def rock_spawner():
    """ A timer handler that spawns asteroids, debris, and lifeforms. """

    if (in_play and 
        not my_ship.at_mothership and 
        len(all_rocks) < max_asteroids):

        random_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        random_vel = [
        randrange_nozero(-max_asteroid_speed, max_asteroid_speed + 1) / 10.0, 
        randrange_nozero(-max_asteroid_speed, max_asteroid_speed + 1) / 10.0]
        random_ang_vel = randrange_nozero(-20, 20) / 100.0
        random_rock = random.randrange(0, 7)

        if dist(my_ship.pos, random_pos) > safe_spawn_distance:
            if random_rock  <= 3:
                asteroid = Sprite(
                    'asteroid', 
                    asteroid_image, 
                    asteroid_info, 
                    random_pos, 
                    random_vel, 
                    0, 
                    random_ang_vel, 
                    False)
                all_rocks.add(asteroid)
            elif random_rock == 4:
                debris = Sprite(
                    'debris', 
                    debris_image, 
                    debris_info, 
                    random_pos, 
                    random_vel, 
                    0, 
                    random_ang_vel, 
                    False)
                all_rocks.add(debris)
            else:
                lifeform = Sprite(
                    'lifeform', 
                    lifeform_image, 
                    lifeform_info, 
                    random_pos, 
                    random_vel, 
                    0, 
                    random_ang_vel, 
                    False)
                all_rocks.add(lifeform)


def keydown(key):
    global first_time, game_is_paused

    def _dir_right(ship):
        if ship.is_left:
            ship.angle_vel = 0
        else:
            ship.angle_vel = ship_turn_vel
        ship.is_right = True

    def _dir_left(ship):
        if ship.is_right:
            ship.angle_vel = 0
        else:
            ship.angle_vel = -ship_turn_vel
        ship.is_left = True

    # splash screen controls
    if first_time and key == 32:
        next_story_board()
    elif game_is_paused and key == 32:
        start_next_level()

    # my_ship controls
    if in_play and key == 37:
        _dir_left(my_ship)
    if in_play and key == 39:
        _dir_right(my_ship)
    if in_play and key == 49 and not my_ship.at_mothership:
        my_ship.fire_missile('disruptor')
    if in_play and key == 50 and not my_ship.at_mothership:
        my_ship.fire_missile('teleporter')
    if in_play and key == 38:
        my_ship.thrust = True
        my_ship.image_centre[0] += ship_info.size[0]
        ship_thrust_sound.rewind()
        ship_thrust_sound.play()


def keyup(key):

    def _dir_right(ship):
        if ship.is_left:
            ship.angle_vel = -ship_turn_vel
        else:
            ship.angle_vel = 0
        ship.is_right = False

    def _dir_left(ship):
        if ship.is_right:
            ship.angle_vel = ship_turn_vel
        else:
            ship.angle_vel = 0
        ship.is_left = False

    # my_ship controls
    if in_play and key == 37:
        _dir_left(my_ship)
    if in_play and key == 39:
        _dir_right(my_ship)
    if in_play and key == 38:
        my_ship.thrust = False
        my_ship.image_centre[0] -= ship_info.size[0]
        ship_thrust_sound.pause()


def mouse_click(position):
    # splash screen controls
    if first_time:
        next_story_board()
    elif game_is_paused:
        start_next_level()


def main_handler():
    """ Timed checks that need not be checked as often as the draw handler. """
    global rescued_this_turn, anomoly_mass, total_score, hull_integrity

    # check if the user has died
    if hull_integrity <= 0 and not game_is_paused:
        end_game()
        game_over()

    # check if the user has passed a level
    if anomoly_mass <= 0:
        end_game()
        if not at_level_status:
            level_status()

    # check if my_ship is at the mothership dimension
    if my_ship.dim_coord == mothership.dim_coord:
        my_ship.at_mothership = True
        my_map.found_mothership = True
        clear_all_types()
    else:
        my_ship.at_mothership = False

    # update the score values if ship is inside the mothership teleport circle
    if (my_ship.at_mothership and 
        dist(CENTRE, my_ship.pos) <= 50 and 
        my_ship.life_forms > 0):
        rescued_this_turn = True
        my_ship.life_forms -= 1
        my_ship.score += 1
        score_sound.rewind()
        score_sound.play()
        total_score += 1
        anomoly_mass -= 10
        if anomoly_mass < 0:
            anomoly_mass = 0

    # relocate the mothership if lifeforms have been rescued
    elif (my_ship.at_mothership and 
          dist(CENTRE, my_ship.pos) > 50 and 
          rescued_this_turn):
        while my_ship.dim_coord == mothership.dim_coord:
            mothership.relocate()
        my_map.found_mothership = False
        rescued_this_turn = False

    # prepare tags for sprite removal
    remove_rocks = set([])
    remove_disruptors = set([])
    remove_teleporters = set([])
    remove_explosions = set([])
    remove_teleports = set([])

    # destroy all rocks hit by ship
    for rock in all_rocks:
        if my_ship.collide(rock):
            if rock.kind == 'asteroid':
                hull_integrity -= 1
                remove_rocks.add(rock)
                asteroid_collision(rock)
            elif rock.kind == 'debris':
                hull_integrity -= 1
                remove_rocks.add(rock)
                debris_collision(rock)
            elif rock.kind == 'powerup':
                hull_integrity += 1
                powerup_sound.rewind()
                powerup_sound.play()
                remove_rocks.add(rock)
            elif rock.kind == 'lifeform':
                # life forms do not collide with the ship
                pass

    # destroy all rocks hit by disruptors
    for rock in all_rocks:
        for disruptor in all_disruptors:
            if rock.collide(disruptor) and rock.kind != 'powerup':
                remove_rocks.add(rock)
                remove_disruptors.add(disruptor)
                anomoly_mass -= 1
                if rock.kind == 'asteroid':
                    asteroid_explosion(rock)
                elif rock.kind == 'debris':
                    debris_explosion(rock)
                elif rock.kind == 'lifeform':
                    lifeform_explosion(rock)

    # transport all rocks hit by teleporter missiles
    for rock in all_rocks:
        for teleporter in all_teleporters:
            if teleporter.collide(rock) and rock.kind != 'powerup':
                remove_rocks.add(rock)
                remove_teleporters.add(teleporter)
                if rock.kind == 'asteroid':
                    # teleporting an asteroid kills all life forms on the ship
                    if my_ship.life_forms > 0:
                        lifeform_death_sound.rewind()
                        lifeform_death_sound.play()
                    my_ship.life_forms = 0
                    asteroid_teleport(rock)
                elif rock.kind == 'debris':
                    # 10% chance that teleporting spaceship debris will reveal
                    # the location of the mothership.
                    if random.randrange(0, 11) == 10:
                        my_map.found_mothership = True
                    debris_teleport(rock)
                elif rock.kind == 'lifeform':
                    # teleport one life form onto the ship
                    my_ship.life_forms += 1
                    lifeform_teleport(rock)

    # control the lifespan of explosions
    for explosion in all_explosions:
        explosion.life += 1
        if explosion.life >= explosion.lifespan:
            remove_explosions.add(explosion)

    # control the lifespan of teleports
    for teleport in all_teleports:
        teleport.life += 1
        if teleport.life >= teleport.lifespan:
            remove_teleports.add(teleport)

    # control the lifespan of all disruptor missiles
    for disruptor in all_disruptors:
        disruptor.life += 1
        if disruptor.life >= disruptor.lifespan:
            remove_disruptors.add(disruptor)

    # control the lifespan of teleporter missiles
    for teleporter in all_teleporters:
        teleporter.life += 1
        if teleporter.life >= teleporter.lifespan:
            remove_teleporters.add(teleporter)

    # remove tagged sprites
    all_rocks.difference_update(remove_rocks)
    all_disruptors.difference_update(remove_disruptors)
    all_explosions.difference_update(remove_explosions)
    all_teleporters.difference_update(remove_teleporters)
    all_teleports.difference_update(remove_teleports)


def draw(canvas):
    """ CodeSkulptor draw handler. """
    global time, levels_remaining
    
    # draw animated background
    time += 1
    wtime = (time / 4) % WIDTH
    centre = grid_info.get_centre()
    size = grid_info.get_size()
    canvas.draw_image(
        nebula_image, 
        nebula_info.get_centre(), 
        nebula_info.get_size(), 
        [WIDTH / 2, HEIGHT / 2], 
        [WIDTH, HEIGHT])
    canvas.draw_image(
        grid_image, 
        centre, 
        size, 
        (wtime - WIDTH / 2, HEIGHT / 2), 
        (WIDTH, HEIGHT))
    canvas.draw_image(
        grid_image, 
        centre, 
        size, 
        (wtime + WIDTH / 2, HEIGHT / 2), 
        (WIDTH, HEIGHT))

    # control the animation of explosions and teleports
    for explosion in all_explosions:
        explosion.step_animate()
    for teleport in all_teleports:
        teleport.step_animate()

    # draw the lower mothership
    if my_ship.at_mothership:
        canvas.draw_image(
            mothership_low_image, 
            mothership_low_info.get_centre(), 
            mothership_low_info.get_size(), 
            [WIDTH / 2, HEIGHT / 2], 
            mothership_low_info.get_size())

    # update and draw the ship
    if hull_integrity > 0:
        my_ship.update()
        my_ship.draw(canvas)
    else:
        end_game()

    # update and draw the asteroids
    for rock in all_rocks:
        rock.update()
        rock.draw(canvas)

    # update and draw all disruptors
    for disruptor in all_disruptors:
        disruptor.update()
        disruptor.draw(canvas)

    # update and draw all teleporters
    for teleporter in all_teleporters:
        teleporter.update()
        teleporter.draw(canvas)

    # update and draw all explosions
    for explosion in all_explosions:
        explosion.update()
        explosion.draw(canvas)

    # update and draw all teleports
    for teleport in all_teleports:
        teleport.update()
        teleport.draw(canvas)

    # draw the upper mothership
    if my_ship.at_mothership:
        canvas.draw_image(
            mothership_high_image, 
            mothership_high_info.get_centre(), 
            mothership_high_info.get_size(), 
            [WIDTH / 2, HEIGHT / 2], 
            mothership_high_info.get_size())

    # draw user interface
    canvas.draw_image(
        interface_top_image, 
        interface_top_info.get_centre(), 
        interface_top_info.get_size(), 
        [WIDTH / 2, interface_top_info.get_size()[1] / 2], 
        interface_top_info.get_size())
    canvas.draw_image(
        interface_bottom_image, 
        interface_bottom_info.get_centre(), 
        interface_bottom_info.get_size(), 
        [WIDTH / 2, HEIGHT - (interface_bottom_info.get_size()[1] / 2)], 
        interface_bottom_info.get_size())
    canvas.draw_text(
        str(hull_integrity), 
        [105, 19], 
        ui_size, 
        ui_colour, 
        ui_font)
    canvas.draw_text(
        str(my_ship.life_forms), 
        [317, 19], 
        ui_size, 
        ui_colour, 
        ui_font)
    canvas.draw_text(
        str(my_ship.score), 
        [523, 19], 
        ui_size, 
        ui_colour, 
        ui_font)
    canvas.draw_text(
        str(anomoly_mass), 
        [690, 19], 
        ui_size, 
        ui_colour, 
        ui_font)
    if beat_the_game:
        levels_remaining = 0
    canvas.draw_text(
        str(levels_remaining), 
        [398, 590], 
        ui_size,
        ui_level_colour, 
        ui_font)

    # draw the map
    my_map.draw(canvas)

    # draw the splash screen
    if game_is_paused:
        canvas.draw_image(
            splash_image, 
            splash_info.get_centre(), 
            splash_info.get_size(), 
            CENTRE, 
            splash_info.get_size())

    # check if the user is at the level status screen
    if at_level_status and not beat_the_game:
        canvas.draw_text(
            str(my_ship.score), 
            [435, 333], 
            status_size, 
            status_colour, 
            status_font)

    # check if the user is at the beat game screen
    if beat_the_game:
        canvas.draw_text(
            str(total_score), 
            [435, 351], 
            status_size, 
            status_colour, 
            status_font)

    # check if the user is starting the game for the first time
    if first_time:
        canvas.draw_image(
            story_image, 
            story_info.get_centre(), 
            story_info.get_size(), 
            CENTRE, 
            story_info.get_size())


#
# INITIALISE CODESKULPTOR FRAME
# _____________________________________________________________________________
# _____________________________________________________________________________
# _____________________________________________________________________________

try:
    frame = simplegui.create_frame("Rescape", WIDTH, HEIGHT, CTRL_WIDTH)
except:
    print "*******************************************"
    print "There was a problem initialising the frame."
    print "Please try pressing the RUN button again."
    print "*******************************************"


#
# REGISTER EVENT HANDLERS
# _____________________________________________________________________________
# _____________________________________________________________________________
# _____________________________________________________________________________


# frame
frame.set_draw_handler(draw)

# timers
main_timer = simplegui.create_timer(main_eh_frequency, main_handler)
asteroid_timer = simplegui.create_timer(rock_spawner_frequency, rock_spawner)
music_timer = simplegui.create_timer(music_frequency, play_music)
victory_timer = simplegui.create_timer(victory_frequency, play_victory)

# input
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(mouse_click)


#
# INITIATE PROGRAM
# _____________________________________________________________________________
# _____________________________________________________________________________
# _____________________________________________________________________________


# call new_game to establish variables
new_game([2, 2], 100, False)

# start timers
main_timer.start()
asteroid_timer.start()
music_timer.start()

# start music
music.play()

# start CodeSkulptor frame
frame.start()

