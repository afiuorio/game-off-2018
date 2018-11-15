import sys

from tcod import libtcod

from interface.gui import Message


class Event:
    def __init__(self, name, info=None, origin=None):
        self.name = name
        self.info = info
        self.origin = origin
        self.handle = event_to_handler[name]

    def handle(self):
        self.handle()

    @staticmethod
    def exit_game_handler(game, event_data, origin):
        sys.exit()

    @staticmethod
    def player_movement_handler(game, event_data, origin):
        player_new_position = (origin.x + event_data[0], origin.y + event_data[1])
        enemy = game.current_map.is_anyone_at(player_new_position[0], player_new_position[1])
        if enemy:
            game.game_screen.message_log.add_line(Message(enemy.get_infos()))
        elif game.current_map.is_blocked_at(player_new_position[0], player_new_position[1]):
            origin.move_object(event_data)

    @staticmethod
    def monster_movement_handler(game, event_data, origin):
        vector = event_data
        enemy = origin
        enemy_new_position = (enemy.x + vector[0], enemy.y + vector[1])
        if game.current_map.is_anyone_at(enemy_new_position[0], enemy_new_position[1]):
            pass
        elif game.current_map.is_blocked_at(enemy_new_position[0], enemy_new_position[1]):
            enemy.move_object(vector)

    @staticmethod
    def monster_action_handler(game, event_data, origin):
        if event_data is "pip":
            game.game_screen.message_log.add_line(Message(str(origin) + " says: Pip!", libtcod.light_green))

    @staticmethod
    def go_pause_handler(game, event_data, origin):
        game.game_state = game.game_states_map.get("Pause")

    @staticmethod
    def go_active_handler(game, event_data, origin):
        game.game_state = game.game_states_map.get("Active")

    @staticmethod
    def nop_handler(game, event_data, origin):
        pass


event_to_handler = {"exit_game" : Event.exit_game_handler, "player_movement": Event.player_movement_handler,
                    "monster_movement": Event.monster_movement_handler, "monster_action": Event.monster_action_handler,
                    "go_pause": Event.go_pause_handler, "go_active": Event.go_active_handler,
                    "nop": Event.nop_handler,
                    }
