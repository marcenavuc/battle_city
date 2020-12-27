import pygame

from battle_city.config import CELL_HEIGHT, CELL_WIDTH
from battle_city.game_objects.game_object import GameObject
from battle_city.utils import Vector


class Wall(GameObject):
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


class Water(GameObject):
    image = "media/images/water.png"


class Leaves(GameObject):
    image = "media/images/leaves.png"


class Iron(GameObject):
    image = "media/images/iron.png"


class Base(GameObject):
    image = "media/images/base.png"


class Floor(GameObject):
    image = "media/images/floor.png"
