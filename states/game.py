import libtcodpy as libtcod
from collections import deque
from objects.objects import Player

from gui import GameScreen

from objects.map import *
from states.states import *

class Game():
    def __init__(self, is_debug):
        self.game_screen = GameScreen(40, 50, 40)
        self.debug = is_debug

        self.event_queue = deque()

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

    def enqueue_event(self, eventName, eventData):
        self.event_queue.append((eventName, eventData))
    
    def dequeue_event(self):
        return self.event_queue.pop()
    
    def change_game_state(self, newState):
        self.game_state = newState
    
    def run_game(self):
        while not libtcod.console_is_window_closed():
            self.game_screen.render_all(self)

            self.game_state.handle_world(self)
            # handling events
            while self.event_queue:
                (eventName, eventData) = self.dequeue_event()
                # FIXME maybe a dictonary of functions ?
                if(eventName == "exit_game"):
                    sys.exit()
                elif(eventName == "player_movement"):
                    player_new_position = (self.player.x + eventData[0][0], self.player.y + eventData[0][1])
                    enemy = self.current_map.is_anyone_at(player_new_position[0], player_new_position[1])
                    if enemy:
                        print(enemy.get_infos())
                    elif self.current_map.is_blocked_at(player_new_position[0], player_new_position[1]):
                        self.player.move_object(eventData[0])
                elif(eventName == "monster_movement"):
                    vector = eventData[0]
                    enemy = eventData[1]
                    enemy_new_position = (enemy.x + vector[0], enemy.y + vector[1])
                    if self.current_map.is_anyone_at(enemy_new_position[0], enemy_new_position[1]):
                        pass
                    elif self.current_map.is_blocked_at(enemy_new_position[0], enemy_new_position[1]):
                        enemy.move_object(vector)
                elif(eventName == "monster_action"):
                    if(eventData[0] == "pip"):
                        print(str(eventData[1]) + " says: Pip!")
                #FIXME these should be a static factories        
                elif(eventName == "go_pause"):
                    self.game_state = self.game_states_map.get("Pause")
                elif(eventName == "go_active"):
                    self.game_state = self.game_states_map.get("Active")
