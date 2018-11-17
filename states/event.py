import sys

import libtcodpy as libtcod

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
            """self.origin.attack_target(enemy)
            damage = self.origin.attack - enemy.defense
            game.game_screen.message_log.add_line(Message("You attack " + enemy.name + " for " + str(damage) + " damage!"))"""
            self.attack(game)
        elif game.current_map.is_blocked_at(player_new_position[0], player_new_position[1]):
            self.origin.move_object(self.info)

    def monster_movement_handler(self, game):
        vector = self.info
        monster = self.origin
        enemy_new_position = (monster.x + vector[0], monster.y + vector[1])
        entity = game.current_map.is_anyone_at(enemy_new_position[0], enemy_new_position[1])
        if entity is game.player:
            game.game_screen.message_log.add_line(Message(self.origin.name + " meekly boops you."))
        elif entity:
            pass
        elif game.current_map.is_blocked_at(enemy_new_position[0], enemy_new_position[1]):
            monster.move_object(vector)

    def monster_aggressive_movement_handler(self, game):
        vector = self.info
        monster = self.origin
        enemy_new_position = (monster.x + vector[0], monster.y + vector[1])
        entity = game.current_map.is_anyone_at(enemy_new_position[0], enemy_new_position[1])
        if entity is game.player:
            self.attack(game)
        elif entity:
            pass
        elif game.current_map.is_blocked_at(enemy_new_position[0], enemy_new_position[1]):
            monster.move_object(vector)

    def monster_action_handler(self, game):
        game.game_screen.message_log.add_line(Message(str(self.origin) + " says: " + self.info + "!", libtcod.light_green))

    def go_pause_handler(self, game):
        game.game_state = game.game_states_map.get("Pause")

    def go_active_handler(self, game):
        game.game_state = game.game_states_map.get("Active")

    def go_game_over_handler(self, game):
        libtcod.console_wait_for_keypress(True)
        game.game_state = game.game_states_map.get("Game Over")

    def nop_handler(self, game):
        pass

    def death_handler(self, game):
        game.game_screen.message_log.add_line(Message(str(self.origin) + " died!", libtcod.light_red))
        game.current_map.entity_list.remove(self.origin)

    def attack(self, game):
        target_coordinates = (self.origin.x + self.info[0], self.origin.y + self.info[1])
        target = game.current_map.is_anyone_at(target_coordinates[0], target_coordinates[1])
        subject = "you" if self.origin is game.player else self.origin.name
        if target:
            self.origin.attack_target(target)
            target_name = "you" if target.name is "Player" else target.name
            damage = self.origin.attack - target.defense
            game.game_screen.message_log.add_line(
                Message(subject.capitalize() + " hits " + target_name + " for " + str(damage) + " damage!"))
        else:
            game.game_screen.message_log.add_line(
                Message(subject.capitalize() + " swing at the void. That was weird."))



event_to_handler = {"exit_game" : Event.exit_game_handler, "player_movement": Event.player_movement_handler,
                    "monster_movement": Event.monster_movement_handler, "monster_action": Event.monster_action_handler,
                    "monster_aggressive_movement": Event.monster_aggressive_movement_handler,
                    "go_pause": Event.go_pause_handler, "go_active": Event.go_active_handler,
                    "game_over": Event.go_game_over_handler, "nop": Event.nop_handler,
                    "death": Event.death_handler,
                    }
