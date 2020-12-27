import random
from enum import Enum

import pygame
from pygame.sprite import DirtySprite

from battle_city.config import CELL_SIZE
from battle_city.utils import Vector


class GameObject(DirtySprite):
    def __new__(cls, position: Vector, *groups):
        assert hasattr(cls, "image"), "You need to specify image on class"
        new_object = object.__new__(cls)
        if isinstance(new_object, cls):
            new_object.sprite = pygame.image.load(cls.image)
            new_object.sprite = pygame.transform.scale(new_object.sprite, CELL_SIZE)
            new_object.image = pygame.transform.rotate(new_object.sprite, 0)
            new_object.rect = new_object.image.get_rect()
            new_object.rect.x, new_object.rect.y = position.x, position.y
            cls.__init__(new_object, position, *groups)
        return new_object

    def __init__(self, position: Vector, *groups):
        super().__init__(*groups)
        self.position = position

    def __dict__(self):
        return {"x": self.rect.x, "y": self.rect.y}

    def __str__(self):
        return self.__dict__()

    def update(self, event: pygame.event, level, *args):
        pass

    @staticmethod
    def in_borders(position: pygame.rect.Rect, level) -> bool:
        return 0 <= position.x <= level.max_x and 0 <= position.y <= level.max_y


class Directions(Enum):
    UP = Vector(0, -1)
    RIGHT = Vector(1, 0)
    DOWN = Vector(0, 1)
    LEFT = Vector(-1, 0)

    def get_angle(self):
        return {
            self.UP: 0,
            self.RIGHT: -90,
            self.LEFT: 90,
            self.DOWN: 180,
        }.get(self)

    @staticmethod
    def random_direction():
        return random.choice(
            [Directions.UP, Directions.RIGHT, Directions.DOWN, Directions.LEFT]
        )


class Movable(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.speed = 0
        self.direction = Directions.UP

    def move(self, direction: Directions, speed: int = -1) -> pygame.rect.Rect:
        if speed == -1:
            speed = self.speed
        if self.direction != direction:
            angle = direction.get_angle()
            self.image = pygame.transform.rotate(self.sprite, angle)
            self.direction = direction
        step = direction.value * speed
        return self.rect.move(*step)

    def __dict__(self):
        return {
            "x": self.rect.x,
            "y": self.rect.y,
            "direction": self.direction.name
        }
