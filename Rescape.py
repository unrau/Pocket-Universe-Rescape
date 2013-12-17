#
# Pocket Universe: Rescape
# v1.59
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
# DEFINE CONSTANTS
# _____________________________________________________________________________
# _____________________________________________________________________________
# _____________________________________________________________________________


# canvas
WIDTH = 800
HEIGHT = 600
CENTRE = [WIDTH / 2, HEIGHT / 2]
CTRL_WIDTH = 100

# game
SAFE_SPAWN_DISTANCE = 200
DISRUPTOR_SPEED = 12
DISRUPTOR_SPIN = 0.2
DISRUPTOR_LIFESPAN = 10
DISRUPTOR_MAX = 3
TELEPORTER_SPEED = 4
TELEPORTER_LIFESPAN = 20
TELEPORTER_MAX = 1
SHIP_ACCELERATION = 0.2
SHIP_TURN_VEL = 0.1
MAX_ASTEROIDS = 5
MAX_ASTEROID_SPEED = 30
DEFAULT_FRICTION = 0.02
BEAT_LEVEL_FRICTION = 0.1
DEFAULT_HULL_INTEGRITY = 5

# timers
ROCK_SPAWNER_FREQUENCY = 1000
MAIN_EH_FREQUENCY = 60
MUSIC_FREQUENCY = 9953
VICTORY_FREQUENCY = 14765

# user interface
NAME_FONT = "monospace"
NAME_SIZE = 14
NAME_COLOUR = "#ffffff"
UI_FONT = "monospace"
UI_SIZE = 12
UI_COLOUR = "#ffffff"
UI_LEVEL_COLOUR = "#73badb"
STATUS_FONT = "monospace"
STATUS_SIZE = 24
STATUS_COLOUR = "#ffffff"
MAP_POS = [20, 51]


#
# DEFINE AND INITIALISE GAME CONTROL VARIABLES
# _____________________________________________________________________________
# _____________________________________________________________________________
# _____________________________________________________________________________


class GameControl:
    def __init__(self):
        """ Define all game control variables. """

        self.level = 0
        self.time = 0.5
        self.total_score = 0
        self.story_board = 0
        self.anomaly_mass = 0
        self.levels_remaining = 10
        self.num_dimensions = {}
        self.num_dimensions['x'] = 0
        self.num_dimensions['y'] = 0
        self.rescued_this_turn = False
        self.at_level_status = False
        self.beat_the_game = False
        self.first_time = True
        self.is_paused = False
        self.in_play = False
        self.friction = DEFAULT_FRICTION
        self.hull_integrity = DEFAULT_HULL_INTEGRITY
        self.all_rocks = set([])
        self.all_disruptors = set([])
        self.all_explosions = set([])
        self.all_teleporters = set([])
        self.all_teleports = set([])
        self.remove_rocks = set([])
        self.remove_disruptors = set([])
        self.remove_teleporters = set([])
        self.remove_explosions = set([])
        self.remove_teleports = set([])

    def update_total_score(self, increment):
        self.total_score += increment

    def get_total_score(self):
        return self.total_score

    def reset_total_score(self):
        self.total_score = 0

    def update_story_board(self):
        self.story_board += 1

    def get_story_board(self):
        return self.story_board

    def set_paused(self, boolean):
        self.is_paused = boolean

    def update_first_time(self, boolean):
        self.first_time = boolean

    def update_level_status(self, boolean):
        self.at_level_status = boolean

    def update_in_play(self, boolean):
        self.in_play = boolean

    def update_time(self, increment):
        self.time += increment

    def get_time(self):
        return self.time

    def update_levels_remaining(self):
        game.levels_remaining = 10 - game.get_level()

    def set_levels_remaining(self, num):
        self.levels_remaining = num

    def reset_levels_remaining(self):
        self.levels_remaining = 10

    def get_levels_remaining(self):
        return self.levels_remaining

    def set_anomaly_mass(self, num):
        self.anomaly_mass = num

    def reduce_anomaly_mass(self, decrement):
        self.anomaly_mass -= decrement

    def get_anomaly_mass(self):
        return self.anomaly_mass

    def update_rescued_this_turn(self, boolean):
        self.rescued_this_turn = boolean

    def update_beat_the_game(self, boolean):
        self.beat_the_game = boolean

    def update_num_dimensions_x(self, num):
        self.num_dimensions['x'] = num

    def get_num_dimensions_x(self):
        return self.num_dimensions['x']

    def update_num_dimensions_y(self, num):
        self.num_dimensions['y'] = num

    def get_num_dimensions_y(self):
        return self.num_dimensions['y']

    def update_friction(self, num):
        self.friction = num

    def get_friction(self):
        return self.friction

    def update_hull_integrity(self, amount):
        self.hull_integrity += amount

    def set_hull_integrity(self, num):
        self.hull_integrity = num

    def get_hull_integrity(self):
        return self.hull_integrity

    def update_level(self, increment):
        self.level += increment

    def reset_level(self):
        self.level = 0

    def get_level(self):
        return self.level

    def add_rock(self, this_object):
        self.all_rocks.add(this_object)

    def add_disruptor(self, this_object):
        self.all_disruptors.add(this_object)

    def add_explosion(self, this_object):
        self.all_explosions.add(this_object)

    def add_teleporter(self, this_object):
        self.all_teleporters.add(this_object)

    def add_teleport(self, this_object):
        self.all_teleports.add(this_object)

    def remove_rock(self, this_object):
        self.remove_rocks.add(this_object)

    def remove_disruptor(self, this_object):
        self.remove_disruptors.add(this_object)

    def remove_explosion(self, this_object):
        self.remove_explosions.add(this_object)

    def remove_teleporter(self, this_object):
        self.remove_teleporters.add(this_object)

    def remove_teleport(self, this_object):
        self.remove_teleports.add(this_object)

    def reset_removal_sets(self):
        self.remove_rocks = set([])
        self.remove_disruptors = set([])
        self.remove_teleporters = set([])
        self.remove_explosions = set([])
        self.remove_teleports = set([])

    def remove_all_from_sets(self):
        self.all_rocks.difference_update(self.remove_rocks)
        self.all_disruptors.difference_update(self.remove_disruptors)
        self.all_explosions.difference_update(self.remove_explosions)
        self.all_teleporters.difference_update(self.remove_teleporters)
        self.all_teleports.difference_update(self.remove_teleports)


# initialise game control object        
game = GameControl()


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


def clear_all_sprites(this_set):
    """ Remove all sprites in a given set. """
    remove_sprites = set([])
    for sprite in this_set:
        remove_sprites.add(sprite)
    this_set.difference_update(remove_sprites)


def clear_all_types():
    """ Remove all sprites from all sets. """
    clear_all_sprites(game.all_disruptors)
    clear_all_sprites(game.all_teleporters)
    clear_all_sprites(game.all_rocks)
    clear_all_sprites(game.all_explosions)
    clear_all_sprites(game.all_teleports)


def end_game(stop_play = True):
    """ Stop the game and reset variables. """
    my_ship.update_thrust(False)
    my_ship.update_is_right(False)
    my_ship.update_is_left(False)
    game.update_friction(BEAT_LEVEL_FRICTION)
    my_ship.set_angle_vel(0)
    game.update_rescued_this_turn(False)
    my_map.update_found_mothership(False)
    ship_thrust_sound.pause()
    ship_thrust_sound.rewind()
    clear_all_types()
    if stop_play:
        game.update_in_play(False)


def game_over():
    """ Display the Game Over splash screen and reset variables. """
    global splash_image
    game.reset_level()
    game.reset_total_score()
    splash_image = splash_image_game_over
    game.set_paused(True)
    game.update_beat_the_game(False)
    die_sound.rewind()
    die_sound.play()
    game_over_sound.rewind()
    game_over_sound.play()


def new_game(dim, mass, play_now = True):
    """ Reset ship, mothership, variables, and create a new game and map. """
    global my_map, my_ship, mothership, splash_image

    if play_now:
        game.update_in_play(True)
        game.update_beat_the_game(False)
        game.set_paused(False)
        game.update_level_status(False)
        splash_image = splash_image_blank
        game.update_friction(DEFAULT_FRICTION)
        if game.level == 1:
            game.set_hull_integrity(DEFAULT_HULL_INTEGRITY)

    game.set_anomaly_mass(mass)

    # num_dimensions x and y must both be even numbers with a maximum of 20
    game.update_num_dimensions_x(dim[0])
    game.update_num_dimensions_y(dim[1])

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
        0, 
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
    global splash_image
    end_game(False)
    game.set_paused(True)
    game.update_levels_remaining()
    if game.level < 10 and not game.beat_the_game:
        # display the normal level status screen
        game.update_level_status(True)
        splash_image = splash_image_level_status
        level_complete_sound.rewind()
        level_complete_sound.play()
    else:
        # display the beat-game status screen
        game.update_beat_the_game(True)
        game.reset_level()
        splash_image = splash_image_beat_game
        beat_game_sound.rewind()
        beat_game_sound.play()
        music_timer.stop()
        music.pause()
        victory_timer.start()
        victory_music.play()


def start_next_level():
    """ Prepare and start the next level. """
    global nebula_image
    nebula_image = nebula_list[game.get_level()]
    transmission_2.pause()
    game.update_level(1)
    if game.level == 1:
        game.reset_levels_remaining()
    new_game(
        [game.get_level() * 2, game.get_level() * 2], 
        game.get_level() * 100)
    level_start_sound.rewind()
    level_start_sound.play()


def next_story_board():
    """ Display the next story board screen. """
    global story_image
    game.update_story_board()
    if game.story_board > 5:
        game.update_first_time(False)
        start_next_level()
    else:
        if game.story_board == 1:
            transmission_1.rewind()
            transmission_1.play()
        else:
            transmission_1.pause()
            transmission_2.rewind()
            transmission_2.play()
        story_image = story_image_list[game.get_story_board()]


def misfire():
    misfire_sound.rewind()
    misfire_sound.play()


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
        self.centre = [size[0] / 2, size[1] / 2]
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
        self.life = 0
        self.dim_coord = [0, 0]
        self.score = 0
        self.life_forms = 0
        self.lighting = lighting
        if sound:
            sound.rewind()
            sound.play()

    def get_nose_pos(self):
        """ Calculate the current position of this sprite's nose. """
        # calculate the position of the ship's nose
        return [(self.get_radius() * 
                 math.cos(self.get_angle()) + 
                 self.get_pos()[0]),
                (self.get_radius() * 
                 math.sin(self.get_angle()) + 
                 self.get_pos()[1])]

    def get_missile_vel(self, kind):
        # set missile velocity based on ship direction and velocity
        if kind == 'disruptor':
            return [((angle_to_vector(self.get_angle())[0] * DISRUPTOR_SPEED) 
                      + self.get_vel()[0]), 
                    ((angle_to_vector(self.get_angle())[1] * DISRUPTOR_SPEED) 
                      + self.get_vel()[1])]
        elif kind == 'teleporter':
            return [((angle_to_vector(self.get_angle())[0] * TELEPORTER_SPEED) 
                      + self.get_vel()[0]), 
                    ((angle_to_vector(self.get_angle())[1] * TELEPORTER_SPEED) 
                      + self.get_vel()[1])]

    def fire_missile(self, missile_kind):
        """ Fire a missile of a given kind. """

        if missile_kind == 'disruptor':
            # create a new disruptor missile
            if len(game.all_disruptors) < DISRUPTOR_MAX:
                disruptor = Sprite(
                    'disruptor', 
                    disruptor_image, 
                    disruptor_info, 
                    self.get_nose_pos(), 
                    self.get_missile_vel('disruptor'), 
                    self.get_angle(), 
                    0, 
                    False, 
                    disruptor_sound)
                # add new missile to the game
                game.add_disruptor(disruptor)
            else:
                # misfire if maximum disruptor shots are in play
                misfire()

        elif missile_kind == 'teleporter':
            # create a new teleporter missile
            if len(game.all_teleporters) < TELEPORTER_MAX:
                teleporter = Sprite(
                    'teleporter', 
                    teleporter_image, 
                    teleporter_info, 
                    self.get_nose_pos(), 
                    self.get_missile_vel('teleporter'), 
                    self.get_angle(), 
                    DISRUPTOR_SPIN, 
                    False,
                    teleporter_sound)
                # add new teleportens to the game
                game.add_teleporter(teleporter)
            else:
                # misfire if maximum teleporter shots are in play
                misfire()

    def get_kind(self):
        return self.kind

    def get_radius(self):
        return self.radius

    def get_pos(self):
        return self.pos

    def get_dim_coord(self):
        return self.dim_coord

    def get_vel(self):
        return self.vel

    def get_forward_vel(self):
        return self.forward_vel

    def get_angle(self):
        return self.angle

    def set_angle_vel(self, num):
        self.angle_vel = num

    def get_angle_vel(self):
        return self.angle_vel

    def get_dim_coord(self):
        return self.dim_coord

    def get_image_centre(self):
        return self.image_centre

    def get_image_size(self):
        return self.image_size

    def update_pos_changed(self, boolean):
        self.pos_changed = boolean

    def update_centre_x(self, amount):
        self.image_centre[0] += amount

    def update_thrust(self, boolean):
        self.thrust = boolean

    def update_is_left(self, boolean):
        self.is_left = boolean

    def update_is_right(self, boolean):
        self.is_right = boolean

    def update_at_mothership(self, boolean):
        self.at_mothership = boolean

    def update_life(self, increment):
        self.life += increment

    def update_score(self, increment):
        self.score += increment

    def get_score(self):
        return self.score

    def update_life_forms(self, amount):
        self.life_forms += amount

    def get_life_forms(self):
        return self.life_forms

    def relocate(self, random_dim = True, x = 0, y = 0):
        """ Move this sprite to a random dimentional coordinate. """
        if random_dim:
            # relocate sprite to random dim-coords within current dimension
            x = random.randrange(0, game.get_num_dimensions_x())
            y = random.randrange(0, game.get_num_dimensions_y())
        self.dim_coord[0] = x
        self.dim_coord[1] = y
        my_map.update_tile(self.get_kind())
        self.update()

    def collide(self, this_sprite):
        """ Return true if this sprite collides with a given sprite. """
        if (dist(this_sprite.get_pos(), self.get_pos()) < 
            this_sprite.get_radius() + self.get_radius()):
            return True

    def step_animate(self):
        """ Set the image of this sprite to the next animation frame. """
        self.image_centre[0] += self.get_image_size()[0]
    
    def update(self):
        """ Update this sprite (called from the draw handler). """
        if self.kind == 'ship':

            # update directional velocity
            self.forward_vel[0] = angle_to_vector(self.get_angle())[0]
            self.forward_vel[1] = angle_to_vector(self.get_angle())[1]

            # update volocity as per thrust
            if self.thrust:
                self.vel[0] += self.get_forward_vel()[0] * SHIP_ACCELERATION
                self.vel[1] += self.get_forward_vel()[1] * SHIP_ACCELERATION

            # update velocity as per friction
            self.vel[0] *= (1 - game.get_friction())
            self.vel[1] *= (1 - game.get_friction())

        # update direction
        self.angle += self.get_angle_vel()

        # update position
        self.pos[0] += self.get_vel()[0]
        self.pos[1] += self.get_vel()[1]

        # update dimensional coordinates
        if self.pos[0] < 0:
            self.dim_coord[0] -= 1
            self.dim_coord[0] %= game.get_num_dimensions_x()
            self.update_pos_changed(True)
        if self.pos[0] > WIDTH:
            self.dim_coord[0] += 1
            self.dim_coord[0] %= game.get_num_dimensions_x()
            self.update_pos_changed(True)
        if self.pos[1] < 0:
            self.dim_coord[1] -= 1
            self.dim_coord[1] %= game.get_num_dimensions_y()
            self.update_pos_changed(True)
        if self.pos[1] > HEIGHT:
            self.dim_coord[1] += 1
            self.dim_coord[1] %= game.get_num_dimensions_y()
            self.update_pos_changed(True)

        if self.pos_changed:
            my_map.update_tile(self.get_kind())
            self.update_pos_changed(False)

        # wrap position
        self.pos[0] %= WIDTH
        self.pos[1] %= HEIGHT

    def draw(self, canvas):
        """ Draw this sprite. """
        canvas.draw_image(
            self.image, 
            self.get_image_centre(), 
            self.get_image_size(), 
            self.get_pos(), 
            self.get_image_size(),
            self.get_angle())
        if self.lighting:
            canvas.draw_image(
                lighting_image, 
                lighting_info.get_centre(), 
                lighting_info.get_size(), 
                self.get_pos(), 
                self.get_image_size(),
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
            game.get_num_dimensions_x() * map_tile_info.get_size()[0] + 1, 
            game.get_num_dimensions_y() * map_tile_info.get_size()[1] + 1]
        # re-position the map based on the grid size
        self.pos = list(MAP_POS)
        self.pos[0] += self.get_grid_size()[0] / 2 + self.get_grid_offset()
        self.pos[1] += self.get_grid_size()[1] / 2 + self.get_grid_offset()

    def update_tile(self, tile):
        """ Update the ship and mothership map markers. """
        if tile == 'mothership':
            self.mothership_pos[0] = MAP_POS[0] + (
                map_tile_info.get_size()[0] * mothership.get_dim_coord()[0])
            self.mothership_pos[1] = MAP_POS[1] + (
                map_tile_info.get_size()[1] * mothership.get_dim_coord()[1])
        if tile == 'ship':
            self.my_ship_pos[0] = MAP_POS[0] + (
                map_tile_info.get_size()[0] * my_ship.get_dim_coord()[0])
            self.my_ship_pos[1] = MAP_POS[1] + (
                map_tile_info.get_size()[1] * my_ship.get_dim_coord()[1])

    def get_grid_size(self):
        return self.grid_size

    def get_grid_offset(self):
        return self.grid_offset

    def get_found_mothership(self):
        return self.found_mothership

    def update_found_mothership(self, boolean):
        self.found_mothership = boolean

    def get_centre(self):
        return self.centre

    def get_grid_size(self):
        return self.grid_size

    def get_pos(self):
        return self.pos

    def get_mothership_pos(self):
        return self.mothership_pos

    def get_my_ship_pos(self):
        return self.my_ship_pos

    def draw(self, canvas):
        """ Draw this map. """

        # draw the map
        canvas.draw_image(
            map_image, 
            self.get_centre(), 
            self.get_grid_size(), 
            self.get_pos(), 
            self.get_grid_size(), 
            0)

        # draw the mothership tile
        if my_map.found_mothership:
            canvas.draw_image(
                map_tile_mothership, 
                map_tile_info.get_centre(), 
                map_tile_info.get_size(), 
                self.get_mothership_pos(), 
                map_tile_info.get_size(), 
                0)

        #draw the ship tile
        canvas.draw_image(
            map_tile_ship, 
            map_tile_info.get_centre(), 
            map_tile_info.get_size(), 
            self.get_my_ship_pos(), 
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
    "http://www.chloeunrau.com/stuff/rescape/images/story-1.png")
story_image_2 = simplegui.load_image (
    "http://www.chloeunrau.com/stuff/rescape/images/story-2.png")
story_image_3 = simplegui.load_image (
    "http://www.chloeunrau.com/stuff/rescape/images/story-3.png")
story_image_4 = simplegui.load_image (
    "http://www.chloeunrau.com/stuff/rescape/images/story-4.png")
story_image_5 = simplegui.load_image (
    "http://www.chloeunrau.com/stuff/rescape/images/story-5.png")
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

disruptor_info = ImageInfo([10, 10], 3, DISRUPTOR_LIFESPAN)
disruptor_image = simplegui.load_image(
    "http://www.chloeunrau.com/stuff/rescape/images/disruptor.png")

teleporter_info = ImageInfo([10, 10], 3, TELEPORTER_LIFESPAN)
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

    if (game.in_play and 
        not my_ship.at_mothership and 
        len(game.all_rocks) < MAX_ASTEROIDS):

        random_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        random_vel = [
        randrange_nozero(-MAX_ASTEROID_SPEED, MAX_ASTEROID_SPEED + 1) / 10.0, 
        randrange_nozero(-MAX_ASTEROID_SPEED, MAX_ASTEROID_SPEED + 1) / 10.0]
        random_ang_vel = randrange_nozero(-20, 20) / 100.0
        random_rock = random.randrange(0, 7)

        if dist(my_ship.get_pos(), random_pos) > SAFE_SPAWN_DISTANCE:
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
                game.add_rock(asteroid)
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
                game.add_rock(debris)
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
                game.add_rock(lifeform)


def keydown(key):

    def _dir_right(ship):
        if ship.is_left:
            ship.set_angle_vel(0)
        else:
            ship.set_angle_vel(SHIP_TURN_VEL)
        ship.update_is_right(True)

    def _dir_left(ship):
        if ship.is_right:
            ship.set_angle_vel(0)
        else:
            ship.set_angle_vel(-SHIP_TURN_VEL)
        ship.update_is_left(True)

    # splash screen controls
    if game.first_time and key == 32:
        next_story_board()
    elif game.is_paused and key == 32:
        start_next_level()

    # my_ship controls
    if game.in_play and key == 37:
        _dir_left(my_ship)
    if game.in_play and key == 39:
        _dir_right(my_ship)
    if game.in_play and key == 49 and not my_ship.at_mothership:
        my_ship.fire_missile('disruptor')
    if game.in_play and key == 50 and not my_ship.at_mothership:
        my_ship.fire_missile('teleporter')
    if game.in_play and key == 38:
        my_ship.update_thrust(True)
        my_ship.update_centre_x(ship_info.get_size()[0])
        ship_thrust_sound.rewind()
        ship_thrust_sound.play()


def keyup(key):

    def _dir_right(ship):
        if ship.is_left:
            ship.set_angle_vel(-SHIP_TURN_VEL)
        else:
            ship.set_angle_vel(0)
        ship.update_is_right(False)

    def _dir_left(ship):
        if ship.is_right:
            ship.set_angle_vel(SHIP_TURN_VEL)
        else:
            ship.set_angle_vel(0)
        ship.update_is_left(False)

    # my_ship controls
    if game.in_play and key == 37:
        _dir_left(my_ship)
    if game.in_play and key == 39:
        _dir_right(my_ship)
    if game.in_play and key == 38:
        my_ship.update_thrust(False)
        my_ship.update_centre_x(-ship_info.get_size()[0])
        ship_thrust_sound.pause()


def mouse_click(position):
    # splash screen controls
    if game.first_time:
        next_story_board()
    elif game.is_paused:
        start_next_level()


def main_handler():
    """ Timed checks that need not be checked as often as the draw handler. """

    # check if the user has died
    if game.hull_integrity <= 0 and not game.is_paused:
        end_game()
        game_over()

    # check if the user has passed a level
    if game.anomaly_mass <= 0:
        end_game()
        if not game.at_level_status:
            level_status()

    # check if my_ship is at the mothership dimension
    if my_ship.dim_coord == mothership.dim_coord:
        my_ship.update_at_mothership(True)
        my_map.update_found_mothership(True)
        clear_all_types()
    else:
        my_ship.update_at_mothership(False)

    # update the score values if ship is inside the mothership teleport circle
    if (my_ship.at_mothership and 
        dist(CENTRE, my_ship.get_pos()) <= 50 and 
        my_ship.life_forms > 0):
        game.update_rescued_this_turn(True)
        my_ship.update_life_forms(-1)
        my_ship.update_score(1)
        score_sound.rewind()
        score_sound.play()
        game.update_total_score(1)
        game.reduce_anomaly_mass(10)
        if game.anomaly_mass < 0:
            game.set_anomaly_mass(0)

    # relocate the mothership if lifeforms have been rescued
    elif (my_ship.at_mothership and 
          dist(CENTRE, my_ship.get_pos()) > 50 and 
          game.rescued_this_turn):
        while my_ship.dim_coord == mothership.dim_coord:
            mothership.relocate()
        my_map.update_found_mothership(False)
        game.update_rescued_this_turn(False)

    # prepare tags for sprite removal
    game.reset_removal_sets()

    # destroy all rocks hit by the ship
    for rock in game.all_rocks:
        if my_ship.collide(rock):
            if rock.kind == 'asteroid':
                game.update_hull_integrity(-1)
                game.remove_rock(rock)
                # create an asteroid collision animation
                explosion = Sprite(
                    'explosion', 
                    asteroid_crash_image, 
                    asteroid_crash_info, 
                    rock.get_pos(), 
                    rock.get_vel(), 
                    rock.get_angle(), 
                    rock.get_angle_vel(), 
                    False, 
                    damage_sound)
                game.add_explosion(explosion)
            elif rock.kind == 'debris':
                game.update_hull_integrity(-1)
                game.remove_rock(rock)
                # create a debris collision animation
                explosion = Sprite(
                    'explosion', 
                    debris_crash_image, 
                    debris_crash_info, 
                    rock.get_pos(), 
                    rock.get_vel(), 
                    rock.get_angle(), 
                    rock.get_angle_vel(), 
                    False, 
                    damage_sound)
                game.add_explosion(explosion)
            elif rock.kind == 'powerup':
                game.update_hull_integrity(1)
                powerup_sound.rewind()
                powerup_sound.play()
                game.remove_rock(rock)
            elif rock.kind == 'lifeform':
                # life forms do not collide with the ship
                pass

    # destroy all rocks hit by disruptors
    for rock in game.all_rocks:
        for disruptor in game.all_disruptors:
            if rock.collide(disruptor) and rock.kind != 'powerup':
                game.remove_rock(rock)
                game.remove_disruptor(disruptor)
                game.reduce_anomaly_mass(1)
                if rock.kind == 'asteroid':
                    # create an asteroid explosion animation
                    explosion = Sprite(
                        'explosion', 
                        asteroid_explosion_image, 
                        asteroid_explosion_info, 
                        rock.get_pos(), 
                        rock.get_vel(), 
                        rock.get_angle(), 
                        rock.get_angle_vel(), 
                        False, 
                        explosion_sound)
                    game.add_explosion(explosion)
                elif rock.kind == 'debris':
                    # create a debris explosion animation
                    explosion = Sprite(
                        'explosion', 
                        debris_explosion_image, 
                        debris_explosion_info, 
                        rock.get_pos(), 
                        rock.get_vel(), 
                        rock.get_angle(), 
                        rock.get_angle_vel(), 
                        False, 
                        explosion_sound)
                    game.add_explosion(explosion)
                    # chance to drop a hull-integrity power-up
                    if random.randrange(0, 2) == 1:
                        powerup = Sprite(
                            'powerup', 
                            powerup_image, 
                            powerup_info, 
                            rock.get_pos(), 
                            rock.get_vel(), 
                            rock.get_angle(), 
                            rock.get_angle_vel(), 
                            False)
                        game.add_rock(powerup)
                elif rock.kind == 'lifeform':
                    # create a lifeform explosion animation
                    explosion = Sprite(
                        'explosion', 
                        lifeform_explosion_image, 
                        lifeform_explosion_info, 
                        rock.get_pos(), 
                        rock.get_vel(), 
                        rock.get_angle(), 
                        rock.get_angle_vel(), 
                        False, 
                        explosion_sound)
                    game.add_explosion(explosion)

    # teleport all rocks hit by teleporters
    for rock in game.all_rocks:
        for teleporter in game.all_teleporters:
            if teleporter.collide(rock) and rock.kind != 'powerup':
                game.remove_rock(rock)
                game.remove_teleporter(teleporter)
                if rock.kind == 'asteroid':
                    # teleporting an asteroid kills all life forms on the ship
                    if my_ship.life_forms > 0:
                        lifeform_death_sound.rewind()
                        lifeform_death_sound.play()
                    my_ship.life_forms = 0
                    # create an asteroid teleport animation
                    teleport = Sprite(
                        'teleport', 
                        asteroid_teleport_image, 
                        asteroid_teleport_info, 
                        rock.get_pos(), 
                        rock.get_vel(), 
                        rock.get_angle(), 
                        rock.get_angle_vel(), 
                        False, 
                        teleport_sound)
                    game.add_teleport(teleport)
                elif rock.kind == 'debris':
                    # 10% chance that teleporting spaceship debris will reveal
                    # the location of the mothership.
                    if random.randrange(0, 11) == 10:
                        my_map.update_found_mothership(True)
                    # create a debris teleport animation
                    teleport = Sprite(
                        'teleport', 
                        debris_teleport_image, 
                        debris_teleport_info, 
                        rock.get_pos(), 
                        rock.get_vel(), 
                        rock.get_angle(), 
                        rock.get_angle_vel(), 
                        False, 
                        teleport_sound)
                    game.add_teleport(teleport)
                elif rock.kind == 'lifeform':
                    # teleport one life form onto the ship
                    my_ship.update_life_forms(1)
                    # create a lifeform teleport animation
                    teleport = Sprite(
                        'teleport', 
                        lifeform_teleport_image, 
                        lifeform_teleport_info, 
                        rock.get_pos(), 
                        rock.get_vel(), 
                        rock.get_angle(), 
                        rock.get_angle_vel(), 
                        False, 
                        teleport_sound)
                    game.add_teleport(teleport)

    # control the lifespan of explosions
    for explosion in game.all_explosions:
        explosion.update_life(1)
        if explosion.life >= explosion.lifespan:
            game.remove_explosion(explosion)

    # control the lifespan of teleports
    for teleport in game.all_teleports:
        teleport.update_life(1)
        if teleport.life >= teleport.lifespan:
            game.remove_teleport(teleport)

    # control the lifespan of all disruptor missiles
    for disruptor in game.all_disruptors:
        disruptor.update_life(1)
        if disruptor.life >= disruptor.lifespan:
            game.remove_disruptor(disruptor)

    # control the lifespan of teleporter missiles
    for teleporter in game.all_teleporters:
        teleporter.update_life(1)
        if teleporter.life >= teleporter.lifespan:
            game.remove_teleporter(teleporter)

    # remove tagged sprites
    game.remove_all_from_sets()


def draw(canvas):
    """ CodeSkulptor draw handler. """
    
    # draw animated background
    game.update_time(1)
    wtime = (game.get_time() / 4) % WIDTH
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
    for explosion in game.all_explosions:
        explosion.step_animate()
    for teleport in game.all_teleports:
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
    if game.hull_integrity > 0:
        my_ship.update()
        my_ship.draw(canvas)
    else:
        end_game()

    # update and draw the asteroids
    for rock in game.all_rocks:
        rock.update()
        rock.draw(canvas)

    # update and draw all disruptors
    for disruptor in game.all_disruptors:
        disruptor.update()
        disruptor.draw(canvas)

    # update and draw all teleporters
    for teleporter in game.all_teleporters:
        teleporter.update()
        teleporter.draw(canvas)

    # update and draw all explosions
    for explosion in game.all_explosions:
        explosion.update()
        explosion.draw(canvas)

    # update and draw all teleports
    for teleport in game.all_teleports:
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
        str(game.get_hull_integrity()), 
        [105, 19], 
        UI_SIZE, 
        UI_COLOUR, 
        UI_FONT)
    canvas.draw_text(
        str(my_ship.get_life_forms()), 
        [317, 19], 
        UI_SIZE, 
        UI_COLOUR, 
        UI_FONT)
    canvas.draw_text(
        str(my_ship.get_score()), 
        [523, 19], 
        UI_SIZE, 
        UI_COLOUR, 
        UI_FONT)
    canvas.draw_text(
        str(game.get_anomaly_mass()), 
        [690, 19], 
        UI_SIZE, 
        UI_COLOUR, 
        UI_FONT)
    if game.beat_the_game:
        game.set_levels_remaining(0)
    canvas.draw_text(
        str(game.get_levels_remaining()), 
        [398, 590], 
        UI_SIZE,
        UI_LEVEL_COLOUR, 
        UI_FONT)

    # draw the map
    my_map.draw(canvas)

    # draw the splash screen
    if game.is_paused:
        canvas.draw_image(
            splash_image, 
            splash_info.get_centre(), 
            splash_info.get_size(), 
            CENTRE, 
            splash_info.get_size())

    # draw the level status screen
    if game.at_level_status and not game.beat_the_game:
        canvas.draw_text(
            str(my_ship.get_score()), 
            [435, 333], 
            STATUS_SIZE, 
            STATUS_COLOUR, 
            STATUS_FONT)

    # draw the beat game screen
    if game.beat_the_game:
        canvas.draw_text(
            str(game.get_total_score()), 
            [435, 351], 
            STATUS_SIZE, 
            STATUS_COLOUR, 
            STATUS_FONT)

    # draw the story screen
    if game.first_time:
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

# this try/except statement returns a readable response when a known bug in
# CodeSkulptor occures in Google Chrome.
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
main_timer = simplegui.create_timer(MAIN_EH_FREQUENCY, main_handler)
asteroid_timer = simplegui.create_timer(ROCK_SPAWNER_FREQUENCY, rock_spawner)
music_timer = simplegui.create_timer(MUSIC_FREQUENCY, play_music)
victory_timer = simplegui.create_timer(VICTORY_FREQUENCY, play_victory)

# input
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(mouse_click)


#
# INITIATE PROGRAM
# _____________________________________________________________________________
# _____________________________________________________________________________
# _____________________________________________________________________________


# call new_game with any values above zero to establish my_ship and mothership
new_game([2, 2], 100, False)

# start timers
main_timer.start()
asteroid_timer.start()
music_timer.start()

# start music
music.play()

# start CodeSkulptor frame
frame.start()

