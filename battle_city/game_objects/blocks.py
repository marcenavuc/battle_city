from battle_city.game_objects.game_object import GameObject


class Block(GameObject):
    pass


class Wall(Block):
    image = "media/images/wall.png"

    def __init__(self, position, *args, **kwars):
        super().__init__(position, *args, **kwars)
        self.health = 4


class Aqua(Block):
    image = "media/images/water.png"


class Iron(Block):
    image = "media/images/iron.png"


class CENTER(Block):
    image = "media/images/base.png"


class GreenBrush(GameObject):
    image = "media/images/leaves.png"


class Floor(GameObject):
    image = "media/images/floor.png"
