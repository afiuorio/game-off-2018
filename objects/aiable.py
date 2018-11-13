from random import choice, randint


class AIObject:
    def __init__(self, algorithm):
        self.algorithm = algorithm

    def act(self):
        return self.algorithm()

    @staticmethod
    def pipsqueak_ai():
        action = randint(0,100)
        if action is 50:
            return ("monster_action", "pip")
        elif 50 <= action <= 99:
            random_direction = choice([(x, y) for x in range(-1, 2) for y in range(-1, 2) if abs(x + y) is 1])
            return ("monster_movement", random_direction)
        else:
            return ("nop", None)
