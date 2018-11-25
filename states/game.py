from objects.objects import Player
import logging

from interface.gui import GameScreen

from objects.map import *
from objects.choicetext import ChoiceText
from objects.menu import *

from states.states import *


class Game():
    def __init__(self, is_debug, debug_room, farm):
        self.game_screen = GameScreen(40, 50, 40)
        self.debug = is_debug
        self.debug_room = debug_room
        self.farm = farm
        self.logger = Game.get_logger(self.debug)

        self.menu_text = ChoiceText("So ur with ur honey and yur making out wen the phone rigns. U anser it n the vioce is \"wut r u doing wit my daughter?\" U tell ur girl n she say \"my dad is ded\". THEN WHO WAS PHONE?", ["Me", "Ur dad", "Linus Torvald, PHD"])
        self.menu = Menu(self.menu_text, 30, 40, 40)

        self.game_states_map = {
            "Active": (ActiveState(), self.game_screen.game_console_wrapper),
            "Pause": (PauseState(), self.game_screen.game_console_wrapper),
            "Game_Over": (GameOverState(), self.game_screen.game_console_wrapper),
            "Menu": (PopUpState(), self.menu.console_wrapper),
        }

        self.change_game_state("Active")
        self.game_screen.current_console = self.game_screen.game_console_wrapper

        self.game_screen_width = self.game_screen.game_console_wrapper.dimensions.get_width()
        self.game_screen_height = self.game_screen.game_console_wrapper.dimensions.get_height()
        self.initialize_game_area(is_debug, debug_room, farm)

    def initialize_game_area(self, is_debug, debug_room, farm):
        if debug_room:
            self.current_map = MapBuilder(0, self.game_screen.current_console.console).make_map_debug(self.game_screen_width, self.game_screen_height)
            starting_position = (int(self.game_screen_width / 4) + 2, int(self.game_screen_height / 4) + 2)
        elif farm:
            self.current_map = MapBuilder(1, self.game_screen.current_console.console).make_map_farm(self.game_screen_width, self.game_screen_height)
            starting_position = (int(self.game_screen_width / 2) - 2, int(self.game_screen_height / 2))
        else:
            self.current_map = MapBuilder(1, self.game_screen.current_console.console).make_map(self.game_screen_width, self.game_screen_height)
            starting_position = self.current_map.get_free_space()

        self.player = Player('@', starting_position[0], starting_position[1], self.game_screen.game_console_wrapper.console)
        self.current_map.entity_list.insert(0, self.player)
        if is_debug:
            self.currentDrawMap = DebugDrawableMap(self.current_map, self.player, self.game_screen.game_console_wrapper.console)
        else:
            self.currentDrawMap = DrawableMap(self.current_map, self.player, self.game_screen.game_console_wrapper.console)

    def change_game_state(self, new_state):
        self.game_state, self.game_screen.current_console = self.game_states_map[new_state]

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
        self.initialize_game_area(self.debug, self.debug_room, self.farm)
