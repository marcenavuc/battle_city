import pygame

from battle_city.config import CELL_WIDTH, CELL_HEIGHT
from battle_city.game_objects.game_object import GameObject
from battle_city.utils import Vector


class Wall(GameObject):
    image = "battle_city/media/images/wall.png"
    HEIGHT = CELL_HEIGHT // 2
    WIDTH = CELL_WIDTH // 2
    SIZE = (HEIGHT, WIDTH)

    def __init__(self, position, *args, **kwars):
        super().__init__(position, *args, **kwars)
        self.image = pygame.transform.scale(self.image, Wall.SIZE)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position.x, position.y


def wall_generator(position: Vector):
    walls = []
    for y in [-Wall.HEIGHT / 2, Wall.HEIGHT / 2]:
        for x in [-Wall.WIDTH / 2, Wall.WIDTH / 2]:
            walls.append(Wall(Vector(position.x + x, position.y + y)))
    return walls


class Water(GameObject):
    image = "battle_city/media/images/water.png"


class Leaves(GameObject):
    image = "battle_city/media/images/leaves.png"


class Iron(GameObject):
    image = "battle_city/media/images/iron.png"


class Base(GameObject):
    image = "battle_city/media/images/base.png"
