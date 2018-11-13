from random import choice, randint

class AIObject:

    # the idea would be to pass the algorithm to the __init__ but I don't know how to do that!
    def act(self):
        return self.random()

    @staticmethod
    def random():
        action = randint(0,100)
        if action is 50:
            return ("monster_action", "pip")
        elif 50 <= action <= 99:
            random_direction = choice([(x, y) for x in range(-1, 2) for y in range(-1, 2) if abs(x + y) is 1])
            return ("monster_movement", random_direction)
        else:
            return ("nop", None)
