class MovableObject:

    def __init__(self, x, y):
        self.x = x;
        self.y = y;
    
    def move_object(self, movement_vector):
        self.x += movement_vector[0]
        self.y += movement_vector[1]