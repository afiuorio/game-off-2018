from random import choice, randint
import libtcodpy as libtcod


class AIObject:
    def __init__(self, algorithm):
        self.algorithm = algorithm

    def act(self, game):
        return self.algorithm(game)

    @staticmethod
    def pipsqueak_ai(game):
        action = randint(0,100)
        if action is 50:
            return ("monster_action", "pip")
        elif 50 <= action <= 99:
            random_direction = choice([(x, y) for x in range(-1, 2) for y in range(-1, 2) if abs(x + y) is 1])
            return ("monster_movement", random_direction)
        else:
            return ("nop", None)

    @staticmethod
    def get_input_act(game):
        key = libtcod.console_wait_for_keypress(True)
        key_map = {
            libtcod.KEY_ESCAPE: ("exit_game", None),
            libtcod.KEY_ENTER: ("go_pause", None),

            libtcod.KEY_UP: ("player_movement", (0, -1)),
            libtcod.KEY_DOWN: ("player_movement", (0, 1)),
            libtcod.KEY_LEFT: ("player_movement", (-1, 0)),
            libtcod.KEY_RIGHT: ("player_movement", (1, 0)),

        }

        return key_map.get(key.vk, ('nop', None))
