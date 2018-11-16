from objects.objects import Player

from interface.gui import GameScreen

from objects.map import *
from states.states import *


class Game():
    def __init__(self, is_debug):
        self.game_screen = GameScreen(40, 50, 40)
        self.debug = is_debug

        self.current_map = MapBuilder(1).make_map(self.game_screen.game_width, self.game_screen.game_height)

        starting_position = self.current_map.get_free_space()
        self.player = Player('@', starting_position[0], starting_position[1])
        self.current_map.entity_list.append(self.player)

        if(is_debug):
            self.currentDrawMap = DebugDrawableMap(self.current_map, self.player)
        else:
            self.currentDrawMap = DrawableMap(self.current_map, self.player)

        self.game_states_map = {
            "Active": ActiveState(),
            "Pause": PauseState(),
        }

        self.game_state = self.game_states_map.get("Active")
    
    def change_game_state(self, newState):
        self.game_state = newState
    
    def run_game(self):
        while not libtcod.console_is_window_closed():
            self.game_screen.render_all(self)

            world_handler = self.game_state.handle_world(self)
            for event in world_handler:
                event.handle(event, self)

