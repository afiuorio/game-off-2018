import sys

from tcod import libtcod

from interface.gui import Message


class Event:
    def __init__(self, name, info=None, origin=None):
        self.name = name
        self.info = info
        self.origin = origin
        # this doesn't work as I'd like but there is a lot behind why it's not a method but remains a function
        # and there is no real gain in spending that much time into learning it rn
        self.handle = event_to_handler[name]

    def handle(self, game):
        self.handle(game)

    def exit_game_handler(self, game):
        sys.exit()

    def player_movement_handler(self, game):
        player_new_position = (self.origin.x + self.info[0], self.origin.y + self.info[1])
        enemy = game.current_map.is_anyone_at(player_new_position[0], player_new_position[1])
        if enemy:
            game.game_screen.message_log.add_line(Message(enemy.get_infos()))
        elif game.current_map.is_blocked_at(player_new_position[0], player_new_position[1]):
            self.origin.move_object(self.info)

    def monster_movement_handler(self, game):
        vector = self.info
        enemy = self.origin
        enemy_new_position = (enemy.x + vector[0], enemy.y + vector[1])
        if game.current_map.is_anyone_at(enemy_new_position[0], enemy_new_position[1]):
            pass
        elif game.current_map.is_blocked_at(enemy_new_position[0], enemy_new_position[1]):
            enemy.move_object(vector)

    def monster_action_handler(self, game):
        if self.info is "pip":
            game.game_screen.message_log.add_line(Message(str(self.origin) + " says: Pip!", libtcod.light_green))

    def go_pause_handler(self, game):
        game.game_state = game.game_states_map.get("Pause")

    def go_active_handler(self, game):
        game.game_state = game.game_states_map.get("Active")

    def nop_handler(self, game):
        pass


event_to_handler = {"exit_game" : Event.exit_game_handler, "player_movement": Event.player_movement_handler,
                    "monster_movement": Event.monster_movement_handler, "monster_action": Event.monster_action_handler,
                    "go_pause": Event.go_pause_handler, "go_active": Event.go_active_handler,
                    "nop": Event.nop_handler,
                    }
