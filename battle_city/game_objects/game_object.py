import random
from enum import Enum
from typing import Dict, Type, Union, List

import pygame
from pygame.sprite import DirtySprite

from battle_city.config import CELL_SIZE
from battle_city.utils import Vector


class GameObject(DirtySprite):
    registry: Dict[str, Type['GameObject']] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__()
        cls.registry[cls.__name__] = cls

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

    def update(self, event: pygame.event, level, *args):
        pass

    @staticmethod
    def is_collide(obj1: "GameObject", obj2: "GameObject"):
        return obj1.rect.colliderect(obj2.rect)

    @staticmethod
    def is_collidelist(obj: Union["GameObject", pygame.rect.Rect],
                       objects: List["GameObject"]) -> int:
        rects = [obj.rect for obj in objects]
        if isinstance(obj, pygame.rect.Rect):
            return obj.collidelist(rects)
        return obj.rect.collidelist(rects)

    @staticmethod
    def in_borders(position: pygame.rect.Rect, level) -> bool:
        return 0 <= position.x <= level.width and 0 <= position.y <= level.height


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
