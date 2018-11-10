# noinspection PyDeprecation
import libtcodpy as libtcod
from collections import deque
from objects.objects import Player

from objects.map import *
from states.states import *

class Game():
    def __init__(self):
        # FIXME this first part should be read from a config file
        SCREEN_WIDTH = 40
        SCREEN_HEIGHT = 40

        libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
        libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'jurassic-mendel', False)
        libtcod.console_set_default_foreground(0, libtcod.white)

        self.event_queue = deque()
        self.game_state = ActiveState()

        # FIXME we start with the room, but it could be anything else

        #self.player = Player('@', 5, 5)

        self.current_map = MapBuilder(1).make_map(SCREEN_WIDTH, SCREEN_HEIGHT)

        starting_position = self.current_map.get_free_space()
        self.player = Player('@', starting_position[0], starting_position[1])

        self.currentDrawMap = DrawableMap(self.current_map, self.player)
    def enqueue_event(self, eventName, eventData):
        self.event_queue.append((eventName, eventData))
    
    def dequeue_event(self):
        return self.event_queue.pop()
    
    def change_game_state(self, newState):
        self.game_state = newState
    
    def run_game(self):
        while not libtcod.console_is_window_closed():
            libtcod.console_clear(0)
            self.game_state.handle_video(self)
            libtcod.console_flush()

            key = libtcod.console_wait_for_keypress(True)
            self.game_state.handle_input(self, key)
            # handling events
            while self.event_queue:
                (eventName, eventData) = self.dequeue_event()
                # FIXME this is perfect for patter matching
                if(eventName == "exit_game"):
                    sys.exit()
                elif(eventName == "player_movement"):
                    player_new_position = (self.player.x + eventData[0], self.player.y + eventData[1])
                    if self.current_map.is_free_at(player_new_position[0], player_new_position[1]):
                        self.player.move_object(eventData)
                elif(eventName == "go_pause"):
                    self.game_state = PauseState()
                elif(eventName == "go_active"):
                    self.game_state = ActiveState()



Game().run_game()