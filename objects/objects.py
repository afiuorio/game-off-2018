from .drawable import DrawableObject
from .movable import MovableObject
from .descriptionobject import DescriptionObject
from .aiable import AIObject


class Entity(DrawableObject, MovableObject, DescriptionObject, AIObject):
    def __init__(self, sprite, x, y, name, description, ai):
        MovableObject.__init__(self, x, y)
        DrawableObject.__init__(self, sprite, x, y)
        DescriptionObject.__init__(self, name, description)
        AIObject.__init__(self, ai)
    
    def __str__(self):
        return self.name


class Player(Entity):
    def __init__(self, sprite, x, y):
        Entity.__init__(self, sprite, x, y, "Player", "A player", AIObject.get_input_act)


class Monster(Entity):
    def __init__(self, sprite, x, y, name, description, ai):
        Entity.__init__(self, sprite, x, y, name, description, ai)

