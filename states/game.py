from objects.objects import Player
import logging

from interface.gui import GameScreen

from objects.map import *
from states.states import *


class Game():
    def __init__(self, is_debug, debug_room):
        self.game_screen = GameScreen(40, 50, 40)
        self.debug = is_debug
        self.debug_room = debug_room
        self.logger = Game.get_logger(self.debug)

        self.initialize_game_area(is_debug, debug_room)

        self.game_states_map = {
            "Active": ActiveState(),
            "Pause": PauseState(),
            "Game Over": GameOverState(),
        }

        self.game_state = self.game_states_map.get("Active")

    def initialize_game_area(self, is_debug, debug_room):
        if debug_room:
            self.current_map = MapBuilder(0).make_map_debug(self.game_screen.game_width, self.game_screen.game_height)
            starting_position = (int(self.game_screen.game_width / 4) + 2, int(self.game_screen.game_height / 4) + 2)
        else:
            self.current_map = MapBuilder(1).make_map(self.game_screen.game_width, self.game_screen.game_height)
            starting_position = self.current_map.get_free_space()
        self.player = Player('@', starting_position[0], starting_position[1])
        self.current_map.entity_list.insert(0, self.player)

        if(is_debug):
        self.current_map.entity_list.append(self.player)
        if is_debug:
            self.currentDrawMap = DebugDrawableMap(self.current_map, self.player)
        else:
            self.currentDrawMap = DrawableMap(self.current_map, self.player)

    def change_game_state(self, newState):
        self.game_state = newState

    @staticmethod
    def get_logger(debug):
            loggerElem = logging.getLogger('game.py')
            if debug:
                loggerElem.setLevel(logging.DEBUG)
                ch = logging.StreamHandler()
                ch.setLevel(logging.DEBUG)
            else: 
                loggerElem.setLevel(logging.INFO)
                ch = logging.StreamHandler()
                ch.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            ch.setFormatter(formatter)
            loggerElem.addHandler(ch)
            logging.basicConfig(filename='jurassic-mendel.log',level=logging.DEBUG)
            return loggerElem

    def run_game(self):
        while not libtcod.console_is_window_closed():
            self.game_screen.render_all(self)

            world_handler = self.game_state.handle_world(self)
            for event in world_handler:
                event.handle(event, self)

    def reset(self):
        self.initialize_game_area(self.debug, self.debug_room)
