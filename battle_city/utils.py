from pygame.math import Vector2


class Vector(Vector2):
    def __init__(self, *args, **kwargs):
        super(Vector, self).__init__(*args, **kwargs)

    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Vector(self.x + other, self.y + other)
        elif isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)
