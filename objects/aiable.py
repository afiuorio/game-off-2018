from random import choice, randint

from interface.gui import Message

import libtcodpy as libtcod


class AIObject:
    def __init__(self, entity):
        self.algorithm, self.check = starting_behavior[entity]

    def act(self, entity, game):
        self.check(entity, game)
        return self.algorithm(entity, game)

    @staticmethod
    def monster_wander(entity, game):
        action = randint(0,100)
        random_direction = (0, 0)
        if action is 50:
            if entity.cry:
                return ("monster_action", entity.cry)
            else:
                return ("nop", None)
        elif 50 <= action <= 99:
            random_direction = choice([(x, y) for x in range(-1, 2) for y in range(-1, 2) if abs(x + y) is 1])

        return ("monster_movement", random_direction)

    @staticmethod
    def follow_and_attack(entity, game):
        step = game.current_map.path_towards_astar(game, entity, entity.nemesis)
        return ("monster_aggressive_movement", step)

    @staticmethod
    def get_input_act(entity, game):
        key = libtcod.console_wait_for_keypress(True)
        key_map = {
            libtcod.KEY_ESCAPE: ("exit_game", None),
            libtcod.KEY_ENTER: ("go_pause", None),

            libtcod.KEY_UP: ("player_movement", (0, -1)),
            libtcod.KEY_DOWN: ("player_movement", (0, 1)),
            libtcod.KEY_LEFT: ("player_movement", (-1, 0)),
            libtcod.KEY_RIGHT: ("player_movement", (1, 0)),

        }

        return key_map.get(key.vk, ("nop", None))

    @staticmethod
    def player_death(entity, game):
        return ("game_over", None)

    @staticmethod
    def death(entity, game):
        return ("death", None)

    @staticmethod
    def passive(entity, game):
        return ("nop", None)

    @staticmethod
    def get_aggro_if_attacked(entity, game):
        if entity.damaged_last_turn:
            print(entity.name + " got pissed!!!")
            entity.check = AIObject.check_nothing
            entity.algorithm = AIObject.follow_and_attack

    @staticmethod
    def get_aggro_on_sight(entity, game):
        # field of view is symmetrical between player and monsters
        if game.currentDrawMap.is_in_fov(entity.x, entity.y):
            print(entity.name + " got pissed!!!")
            game.game_screen.message_log.add_line(
                Message(str(entity.name) + " is pissed!", libtcod.red))
            entity.nemesis = game.player
            entity.check = AIObject.check_nothing
            entity.algorithm = AIObject.follow_and_attack

    @staticmethod
    def check_nothing(entity, game):
        pass


starting_behavior = {"Pipsqueak": (AIObject.monster_wander, AIObject.get_aggro_if_attacked),
                     "Odd Ooze": (AIObject.monster_wander, AIObject.get_aggro_on_sight),
                     "Player": (AIObject.get_input_act, AIObject.check_nothing),
                    }