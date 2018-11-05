from .objects import DrawableObject

class Tiles():
    def __init__(self, block = False):
        self.block = block

class Map():
    def __init__(self, mapX, mapY):
        self.lenght = mapX
        self.height = mapY

        self.mapBuffer = [[ Tiles() for y in range(mapY)] for x in range(mapX)]
    
    def getTile(self, x, y):
        return self.mapBuffer[x][y]

    def isFreeAt(self, x, y):
        return (self.mapBuffer[x][y].block is False)
    
    def draw(self):
        for y in range(self.height):
            for x in range(self.lenght):
                if self.getTile(x,y).block:
                    DrawableObject('#', x, y).draw()
                else:
                    DrawableObject('.', x, y).draw()
