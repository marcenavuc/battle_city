import pygame

from battle_city.config import CELL_HEIGHT, CELL_WIDTH
from battle_city.game_objects.game_object import GameObject
from battle_city.utils import Vector


class Block(GameObject):
    pass


class Wall(Block):
    image = "media/images/wall.png"
    HEIGHT = CELL_HEIGHT // 2
    WIDTH = CELL_WIDTH // 2
    SIZE = (HEIGHT, WIDTH)

    def __init__(self, position, *args, **kwars):
        super().__init__(position, *args, **kwars)
        self.image = pygame.transform.scale(self.image, Wall.SIZE)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position.x, position.y


class Walls:
    def __new__(cls, position: Vector):
        walls = []
        for y in [-Wall.HEIGHT / 2, Wall.HEIGHT / 2]:
            for x in [-Wall.WIDTH / 2, Wall.WIDTH / 2]:
                walls.append(Wall(position + Vector(x, y)))
        return walls


class Aqua(Block):
    image = "media/images/water.png"


class GreenBrush(Block):
    image = "media/images/leaves.png"


class Iron(Block):
    image = "media/images/iron.png"


class CENTER(Block):
    image = "media/images/base.png"


class Floor(GameObject):
    image = "media/images/floor.png"
