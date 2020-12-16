import pygame

from battle_city.config import CELL_SIZE, CELL_WIDTH, CELL_HEIGHT
from battle_city.game_objects.game_object import GameObject
from battle_city.utils import Vector


class Wall(GameObject):
    HEIGHT = CELL_HEIGHT // 2
    WIDTH = CELL_WIDTH // 2
    SIZE = (HEIGHT, WIDTH)

    def __init__(self, position, *args, **kwars):
        super().__init__(position, *args, **kwars)
        self.image = pygame.image.load("battle_city/media/images/wall.png")
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

    def __init__(self, position, *args, **kwars):
        super().__init__(position, *args, **kwars)
        self.image = pygame.image.load("battle_city/media/images/water.png")
        self.image = pygame.transform.scale(self.image, CELL_SIZE)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position.x, position.y


class Leaves(GameObject):

    def __init__(self, position, *args, **kwars):
        super().__init__(position, *args, **kwars)
        self.image = pygame.image.load("battle_city/media/images/leaves.png")
        self.image = pygame.transform.scale(self.image, CELL_SIZE)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position.x, position.y


class Iron(GameObject):

    def __init__(self, position, *args, **kwars):
        super().__init__(position, *args, **kwars)
        self.image = pygame.image.load("battle_city/media/images/iron.png")
        self.image = pygame.transform.scale(self.image, CELL_SIZE)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position.x, position.y


class Base(GameObject):

    def __init__(self, position, *args, **kwars):
        super().__init__(position, *args, **kwars)
        self.image = pygame.image.load("battle_city/media/images/base.png")
        self.image = pygame.transform.scale(self.image, CELL_SIZE)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position.x, position.y
