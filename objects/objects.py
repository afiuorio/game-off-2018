from .drawable import DrawableObject
from .movable import MovableObject
from .descriptionobject import DescriptionObject


class Player(DrawableObject, MovableObject):

    def __init__(self, sprite, x, y):
        MovableObject.__init__(self, x, y)
        DrawableObject.__init__(self, sprite, x, y)


class Monster(DrawableObject, MovableObject, DescriptionObject):

    def __init__(self, sprite, x, y, name, description):
        MovableObject.__init__(self, x, y)
        DrawableObject.__init__(self, sprite, x, y)
        DescriptionObject.__init__(self, name, description)

