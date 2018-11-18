from .objects import DrawableObject
from .objects import Monster
from .objects import AIObject

from random import shuffle, randint, choice
from copy import deepcopy

import libtcodpy as libtcod



class Tiles(DrawableObject):
    def __init__(self, x, y, glyph="", block=False, trasparent=True):
        DrawableObject.__init__(self, glyph, x, y)
        self.block = block
        self.trasparent = trasparent
        self.explored = False
    
    def draw(self):
        if self.explored:
            DrawableObject.draw(self)


class Rectangle:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.x2 = x + w
        self.y1 = y
        self.y2 = y + h

    def intersect(self, rectangle2):
        return (self.x1 <= rectangle2.x2 and self.x2 >= rectangle2.x1
                and self.y1 <= rectangle2.y2 and self.y2 >= rectangle2.y1)

    def get_random_boundary_point(self):
        # I give a number to each side starting from the top one and proceeding in a clockwise order
        side = randint(0, 3)
        if side is 0:
            point = randint(self.x1, self.x2)
            return (point, self.y1)
        elif side is 1:
            point = randint(self.y1, self.y2)
            return (self.x2, point)
        elif side is 2:
            point = randint(self.x1, self.x2)
            return (point, self.y2)
        elif side is 3:
            point = randint(self.y1, self.y2)
            return (self.x1, point)


class Room:
    def __init__(self, x, y, w, h):
        self.dimensions = Rectangle(x, y, w, h)

    def link_to(self, room2):
        start = self.dimensions.get_random_boundary_point()
        end = room2.dimensions.get_random_boundary_point()
        corridor = Corridor(start)
        corridor.link(end)
        return corridor

    def intersect(self, room2):
        self.dimensions.intersect(room2.dimensions)



class Corridor:
    def __init__(self, point):
        self.x = point[0]
        self.y = point[1]
        self.steps = list()

    # the idea would be to pass the strategy as an argument, but I don't know how to make them statics
    # or if we should put them in another class (it would made sense but also they would be used only here...)
    # so for now I just alternate between the two
    def link(self, point):
        if randint(0,3) == 1:
            self.trivial_strategy(self.x, self.y, point[0], point[1])
        else:
            self.fuzzy_strategy(self.x, self.y, point[0], point[1])

    def trivial_strategy(self, x1, y1, x2, y2):
        step1 = 1 if x1 < x2 else -1
        step2 = 1 if y1 < y2 else -1
        self.steps += [(step1, 0) for j in range(x1, x2, step1)]
        self.steps += [(0, step2) for k in range(y1, y2, step2)]

    def fuzzy_strategy(self, x1, y1, x2, y2):
        self.trivial_strategy(x1, y1, x2, y2)
        shuffle(self.steps)


class MapBuilder:
    def __init__(self, depth):
        self.rooms = list()
        self.corridors = list()
        self.depth = depth

    def make_map(self, map_width, map_length):
        self.map = Map(map_width, map_length)
        max_rooms_per_quadrant = (self.depth * 2) + randint(-1, 1)
        big_room = range(1, 20) is 20

        for quadrant in self.map.quadrants.quadrants:
            for i in range(max_rooms_per_quadrant):
                if big_room:
                    self.make_room(quadrant, 10, 15)
                    big_room = False
                else:
                    variance = randint(-2, 4)
                    width = randint(5, 8) + variance
                    height = randint(5, 8) + variance
                    self.make_room(quadrant, width, height)

        shuffle(self.rooms)

        # this is NOT PYTHONIC
        for i in range(len(self.rooms)):
            double_corridor = range(1, 10) is 10
            next_room = 0 if (i+1) is len(self.rooms) else i + 1
            self.corridors.append(self.rooms[i].link_to(self.rooms[next_room]))
            if double_corridor:
                next_room = randint(0, len(self.rooms) - 1)
                if next_room is i:
                    if next_room is len(self.rooms) - 1:
                        next_room -= 1
                    else:
                        next_room += 1
                self.corridors.append(self.rooms[i].link_to(self.rooms[next_room]))

        self.carve_map()
        self.fill_enemies()
        return self.map

    def make_room(self, quadrant, room_width, room_height):
        new_room = Room(randint(quadrant.x1 + 1, quadrant.x2 - room_width - 2), randint(quadrant.y1 + 1, quadrant.y2 - room_height - 2), room_width,
             room_height)
        self.rooms.append(new_room)

    def fill_enemies(self):
        for room in self.rooms:
            enemy_number = (self.depth * 2) + randint(-1, 2)
            for i in range(enemy_number):
                # the +1 / -1 SHOULD fix the bug where sometimes enemies spawn inside walls
                x = randint(room.dimensions.x1+1, room.dimensions.x2-1)
                y = randint(room.dimensions.y1+1, room.dimensions.y2-1)
                while self.map.is_something_at(x, y):
                    x = randint(room.dimensions.x1+1, room.dimensions.x2-1)
                    y = randint(room.dimensions.y1+1, room.dimensions.y2-1)
                if randint(0, 10) < 10:
                    self.map.entity_list.append(Monster("p", x, y, "Pipsqueak", "A friendly small thing", "Pip!",
                                                     5, 4, 1))
                else:
                    self.map.entity_list.append(Monster("O", x, y, "Odd Ooze", "Oddly obstinated ochre ooze", "Fgfsd",
                                                        10, 6, 1))

    def carve_map(self):
        for room in self.rooms:
            for j in range(room.dimensions.x1, room.dimensions.x2):
                for k in range(room.dimensions.y1, room.dimensions.y2):
                    self.map.mapBuffer[j][k] = Tiles(j, k, ".")
        for corridor in self.corridors:
            j, k = corridor.x, corridor.y
            self.map.mapBuffer[j][k] = Tiles(j, k, ".")
            for direction in corridor.steps:
                d1, d2 = direction
                j += d1
                k += d2
                self.map.mapBuffer[j][k] = Tiles(j, k, ".")
        self.map.make_walls()


class Quadrants:
    def __init__(self, rectangle):
        self.quadrants = list()
        first_half_x = int((rectangle.x2 - rectangle.x1) / 2) + ((rectangle.x2 - rectangle.x1) % 2)
        second_half_x = rectangle.x2 - (rectangle.x1 + first_half_x)
        first_half_y = int((rectangle.y2 - rectangle.y1) / 2)  + ((rectangle.x2 - rectangle.x1) % 2)
        second_half_y = rectangle.y2 - (rectangle.y1 + first_half_y)
        self.quadrants.append(Rectangle(rectangle.x1, rectangle.y1, first_half_x - 1, first_half_y - 1))
        self.quadrants.append(Rectangle(rectangle.x1 + first_half_x, rectangle.y1, second_half_x, first_half_y - 1))
        self.quadrants.append(Rectangle(rectangle.x1 + first_half_x, rectangle.y1 + first_half_y, second_half_x, second_half_y))
        self.quadrants.append(Rectangle(rectangle.x1, rectangle.y1 + first_half_y, first_half_x - 1, second_half_y))


class Map:
    def __init__(self, map_x, map_y):
        self.width = map_x
        self.height = map_y
        self.quadrants = Quadrants(Rectangle(0, 0, map_x, map_y))
        self.entity_list = list()
        self.mapBuffer = [[Tiles(x, y, " ", True) for y in range(map_y)] for x in range(map_x)]

    def get_tile(self, x, y):
        return self.mapBuffer[x][y]
    
    def get_map_list(self):
        return [x for sublist in self.mapBuffer for x in sublist]

    def is_blocked_at(self, x, y):
        return (self.mapBuffer[x][y].block is False)

    def is_anyone_at(self, x, y):
        for entity in self.entity_list:
            if entity.x is x and entity.y is y:
                return entity
        return None

    def is_something_at(self, x, y):
        return self.is_blocked_at(x, y) and self.is_anyone_at(x, y)

    # we should check if the values are inside the map
    def make_room(self, x, y, w, h):
        for j in range(x, x + w):
            for k in range(y, y + h):
                self.mapBuffer[j][k] = Tiles(j, k, ".")

    # we should check if the values are inside the map
    def make_corridor(self, x1, y1, x2, y2):
        step1 = 1 if x1 < x2 else -1
        step2 = 1 if y1 < y2 else -1

        for j in range(x1, x2, step1):
            self.mapBuffer[j][y1] = Tiles(j, y1, ".")
        for k in range(y1, y2, step2):
            self.mapBuffer[j][k] = Tiles(j, k, ".")

    def make_walls(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.is_blocked_at(x, y):
                    for j in range(x - 1, x + 2):
                        for k in range(y - 1, y + 2):
                            if not self.is_blocked_at(j, k):
                                self.mapBuffer[j][k] = Tiles(j, k, "#", True, False)

    def get_free_space(self):
        x = randint(1, self.width - 1)
        y = randint(1, self.height - 1)
        while not self.is_blocked_at(x, y) and not self.is_anyone_at(x, y):
            x = randint(1, self.width - 1)
            y = randint(1, self.height - 1)
        return (x, y)

    # tries to return a random cardinal direction towards the target
    # if the target is reached returns None
    # if the next step towards the target is blocked returns (0, 0), meaning to wait
    def get_step_towards(self, origin_x, origin_y, target_x, target_y):
        if self.get_distance(origin_x, origin_y, target_x, target_y) is 1:
            if target_x < origin_x:
                return (-1, 0)
            elif target_x > origin_x:
                return (1, 0)
            elif target_y < origin_y:
                return (0, -1)
            elif target_y > origin_y:
                return (0, 1)
        else:
            dx = 1 if origin_x < target_x else -1 if origin_x > target_x else 0
            dy = 1 if origin_y < target_y else -1 if origin_y > target_y else 0
            vectors = ((dx, 0), (0, dy))
            index = randint(0,1)
            tentative_direction = vectors[index]
            if self.is_anyone_at(origin_x + tentative_direction[0], origin_y + tentative_direction[1]):
                index = 1 - index
                if self.is_anyone_at(origin_x + tentative_direction[0], origin_y + tentative_direction[1]):
                    return (0, 0)
                else:
                    return tentative_direction
            else:
                return tentative_direction

    # FIXME: there is A LOT of optimization and finetuning to do here
    def path_towards_astar(self, game, origin, target):
        # getting the fov vamp from currentDrawMap doesn't work in debug mode since it isn't initialized
        # so for the moment I'm recomputing it every time, it's super wasteful but the game chugs along nicely
        fov = libtcod.map_new(self.width, self.height)

        list(map(lambda tile: libtcod.map_set_properties(fov, tile.x, tile.y, tile.trasparent, not tile.block),
                 self.get_map_list()))

        for entity in self.entity_list:
            if entity != origin and entity != target:
                libtcod.map_set_properties(fov, entity.x, entity.y, True, False)

        my_path = libtcod.path_new_using_map(fov, 0.0)

        libtcod.path_compute(my_path, origin.x, origin.y, target.x, target.y)

        return_direction = (0, 0)
        if not libtcod.path_is_empty(my_path) and libtcod.path_size(my_path) < 30:
            x, y = libtcod.path_walk(my_path, True)
            if x or y:
                x1 = 1 if origin.x < x else -1 if origin.x > x else 0
                y1 = 1 if origin.y < y else -1 if origin.y > y else 0
                return_direction = (x1, y1)
        else:
            return_direction = self.get_step_towards(origin.x, origin.y, target.x, target.y)

        libtcod.path_delete(my_path)
        return return_direction

    # taxicab norm
    def get_distance(self, origin_x, origin_y, target_x, target_y):
        width = abs(origin_x - target_x)
        height = abs(origin_y - target_y)
        return width + height


class DrawableMap():
    def __init__(self, currentMap, player):
        self.currentMap = currentMap
        self.player = player
        self.fov_map = libtcod.map_new(currentMap.width, currentMap.height)
        self.fov_size = 5

        list(map(lambda tile:libtcod.map_set_properties(self.fov_map, tile.x, tile.y, tile.trasparent, not tile.block),
                 currentMap.get_map_list()))

        for tile in self.get_tiles_in_fov(): tile.explored = True
        
    def get_tiles_in_fov(self):
        libtcod.map_compute_fov(self.fov_map, self.player.x, self.player.y, self.fov_size, True, 0)
        return list(filter(lambda tile: libtcod.map_is_in_fov(self.fov_map, tile.x, tile.y), self.currentMap.get_map_list()))

    def get_map(self):
        return self.currentMap
    
    def is_in_fov(self, x, y):
        return libtcod.map_is_in_fov(self.fov_map, x, y)

    def draw(self):
        for tile in self.currentMap.get_map_list():
            tile.draw()
            libtcod.console_set_char_foreground(0, tile.x, tile.y,  libtcod.Color(255, 0, 0))
        
        for tile in self.get_tiles_in_fov():
            self.currentMap.get_tile(tile.x,tile.y).explored = True
            libtcod.console_set_char_foreground(0, tile.x, tile.y, libtcod.Color(255, 255, 255))


class DebugDrawableMap():
    def __init__(self, currentMap, player):
        self.currentMap = currentMap
        self.player = player
        self.fov_map = currentMap
        for tile in self.currentMap.get_map_list():
            tile.explored = True;

    def get_tiles_in_fov(self):
        return self.currentMap.get_map_list()

    def get_map(self):
        return self.currentMap

    def is_in_fov(self, x, y):
        return True

    def draw(self):
        for tile in self.currentMap.get_map_list():
            tile.draw()
            libtcod.console_set_char_foreground(0, tile.x, tile.y, libtcod.Color(255, 255, 255))
