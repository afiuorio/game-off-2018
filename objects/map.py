from .objects import DrawableObject
import libtcodpy as libtcod
from random import shuffle, randint


class Tiles(DrawableObject):
    def __init__(self, x, y, glyph="", block=False, trasparent=True):
        DrawableObject.__init__(self, glyph, x, y)
        self.block = block
        self.trasparent = trasparent


class Room:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def link_to(self, room2):
        x1 = int(self.x + (self.w / 2))
        y1 = int(self.y + (self.h / 2))
        x2 = int(room2.x + (room2.w / 2))
        y2 = int(room2.y + (room2.h / 2))
        corridor = Corridor(x1, y1)
        corridor.link(x2, y2)
        return corridor


class Corridor:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.steps = list()

    # the idea would be to pass the strategy as an argument, but I don't know how to make them statics
    # or if we should put them in another class (it would made sense but also they would be used only here...)
    # so for now I just alternate between the two
    def link(self, x, y):
        if randint(0,3) == 1:
            self.trivial_strategy(self.x, self.y, x, y)
        else:
            self.fuzzy_strategy(self.x, self.y, x, y)

    def trivial_strategy(self, x1, y1, x2, y2):
        step1 = 1 if x1 < x2 else -1
        step2 = 1 if y1 < y2 else -1
        self.steps += [(step1, 0) for j in range(x1, x2, step1)]
        self.steps += [(0, step2) for k in range(y1, y2, step2)]

    def fuzzy_strategy(self, x1, y1, x2, y2):
        self.trivial_strategy(x1, y1, x2, y2)
        shuffle(self.steps)

# Maybe the name isn't the best, but it looks close enough to the real Builder pattern to me
class MapBuilder:
    def __init__(self):
        self.rooms = list()
        self.corridors = list()

    # hardcoded for now, it will be procgen in the future
    def make_map(self, map_width, map_length):
        map = Map(map_width, map_length)
        self.rooms.append(Room(1, 1, 11, 11))
        self.rooms.append(Room(20, 1, 13, 9))
        self.rooms.append(Room(20, 20, 5, 5))
        self.rooms.append(Room(3, 33, 4, 2))
        self.rooms.append(Room(28, 34, 10, 4))
        self.corridors.append(self.rooms[0].link_to(self.rooms[1]))
        self.corridors.append(self.rooms[1].link_to(self.rooms[2]))
        self.corridors.append(self.rooms[1].link_to(self.rooms[3]))
        self.corridors.append(self.rooms[3].link_to(self.rooms[4]))
        self.carve_map(map)
        return map

    def carve_map(self, map):
        for room in self.rooms:
            for j in range(room.x, room.x + room.w):
                for k in range(room.y, room.y + room.h):
                    map.mapBuffer[j][k] = Tiles(j, k, ".")
        for corridor in self.corridors:
            j, k = corridor.x, corridor.y
            map.mapBuffer[j][k] = Tiles(j, k, ".")
            for direction in corridor.steps:
                d1, d2 = direction
                j += d1
                k += d2
                map.mapBuffer[j][k] = Tiles(j, k, ".")
        map.make_walls()


class Map:
    def __init__(self, map_x, map_y):
        self.lenght = map_x
        self.height = map_y


        self.mapBuffer = [[Tiles(x, y, " ", True) for y in range(map_y)] for x in range(map_x)]

    def get_tile(self, x, y):
        return self.mapBuffer[x][y]

    def is_free_at(self, x, y):
        return (self.mapBuffer[x][y].block is False)

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
        for x in range(self.lenght):
            for y in range(self.height):
                if self.is_free_at(x, y):
                    for j in range(x - 1, x + 2, 2):
                        for k in range(y - 1, y + 2, 2):
                            if not self.is_free_at(j, k):
                                self.mapBuffer[j][k] = Tiles(j, k, "#", True, False)


class DrawableMap:
    def __init__(self, map, player):
        self.currentMap = map
        self.player = player
        self.fov_map = libtcod.map_new(map.lenght, map.height)

        for y in range(self.currentMap.height):
            for x in range(self.currentMap.lenght):
                libtcod.map_set_properties(self.fov_map, x, y, self.currentMap.get_tile(x, y).trasparent,
                                           not self.currentMap.get_tile(x, y).block)

    def get_map(self):
        return self.currentMap

    def draw(self):
        libtcod.map_compute_fov(self.fov_map, self.player.x, self.player.y, 10, True, 0)
        for y in range(self.currentMap.height):
            for x in range(self.currentMap.lenght):
                if libtcod.map_is_in_fov(self.fov_map, x, y):
                    self.currentMap.get_tile(x, y).draw()
