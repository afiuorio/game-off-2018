from .drawable import DrawableObject
from .movable import MovableObject
from .descriptionobject import DescriptionObject
from .aiable import AIObject
from .combatable import CombatObject


class Entity(DrawableObject, MovableObject, DescriptionObject, AIObject, CombatObject):
    def __init__(self, sprite, x, y, name, description, cry, ai, hp, attack, defense):
        MovableObject.__init__(self, x, y)
        DrawableObject.__init__(self, sprite, x, y)
        DescriptionObject.__init__(self, name, description, cry)
        AIObject.__init__(self, ai)
        CombatObject.__init__(self, hp, attack, defense)
    
    def __str__(self):
        return self.name


class Player(Entity):
    def __init__(self, sprite, x, y):
        Entity.__init__(self, sprite, x, y, "Player", "A player", "", "Player", 10, 4, 4)

    def dies(self):
        self.algorithm = AIObject.player_death


class Monster(Entity):
    def __init__(self, sprite, x, y, name, description, cry, hp, attack, defense):
        Entity.__init__(self, sprite, x, y, name, description, cry, name, hp, attack, defense)

    def dies(self):
        self.algorithm = AIObject.death


class MonsterFactory:
    def __init__(self, console=0):
        self.console = console

    def make_monster(self, name, x, y):
        sprite, description, cry, hp, attack, defense = self.monster_dictionary[name]
        return Monster(sprite, x, y, name, description, cry, hp, attack, defense)

    monster_dictionary = {"Pipsqueak": ("p", "A friendly small thing", "Pip!", 5, 4, 1),
                          "Odd Ooze": ("O", "Oddly obstinated ochre ooze", "Fgfsd", 10, 6, 1)}

