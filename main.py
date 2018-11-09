# noinspection PyDeprecation
import libtcodpy as libtcod
from collections import deque
from objects.objects import Player
from objects.map import Map, MapBuilder, DrawableMap

#should this function always return something? Probably so since a roguelike proceeds only when the player inputs something
def handle_keys(currentMap, player):
 
    key = libtcod.console_wait_for_keypress(True)
    if key.vk == libtcod.KEY_ESCAPE:
        return "exit"  #exit game

    #movement keys
    if libtcod.console_is_key_pressed(libtcod.KEY_UP) or chr(key.c) == "k":
        return (0, -1)
    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN) or chr(key.c) == "j":
        return (0, 1)
    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT) or chr(key.c) == "h":
        return (-1, 0)
    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT) or chr(key.c) == "l":
        return (1, 0)
    elif chr(key.c) == "y":
    	return (-1, -1)
    elif chr(key.c) == "u":
    	return (1, -1)
    elif chr(key.c) == "b":
    	return (-1, 1)
    elif chr(key.c) == "n":
    	return (1, 1)

    #catch all the other keys, do nothing
    else:
        return (0, 0)


def move_step():
    #this works on the assumption that there is always an element in the queue, and it's the player movement
    player_vector = movement_queue.popleft()

    player_new_position = (player.x + player_vector[0], player.y + player_vector[1])
    if current_map.is_free_at(player_new_position[0], player_new_position[1]):
        player.move_object(player_vector)



SCREEN_WIDTH = 40
SCREEN_HEIGHT = 40

libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'jurassic-mendel', False)

player = Player('@', 5, 5)

map_builder = MapBuilder()
current_map = map_builder.make_map(40, 40)


currentDrawMap = DrawableMap(current_map, player)

movement_queue = deque()

while not libtcod.console_is_window_closed():
    libtcod.console_set_default_foreground(0, libtcod.white)
    currentDrawMap.draw()
    player.draw()
    libtcod.console_flush()

    player.clear()
    command = handle_keys(current_map, player)

    if command is "exit":
        break
    #the only possible action rn is moving so there is no need to check command
    else:
        movement_queue.append(command)

    move_step()
