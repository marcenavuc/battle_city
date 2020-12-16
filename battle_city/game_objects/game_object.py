import pygame
from enum import Enum
#  https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.DirtySprite
from pygame.sprite import DirtySprite
from battle_city.utils import Vector
from battle_city.config import CELL_SIZE


class GameObject(DirtySprite):

    def __init__(self, position: Vector, *groups):
        super().__init__(*groups)
        self.position = position
        self.image = None

    def update(self, event: pygame.event, level, *args):
        pass

    @staticmethod
    def in_borders(position: pygame.rect.Rect, level) -> bool:
        return 0 <= position.x <= level.max_x \
               and 0 <= position.y <= level.max_y


class Directions(Enum):
    UP = Vector(0, -1)
    RIGHT = Vector(1, 0)
    DOWN = Vector(0, 1)
    LEFT = Vector(-1, 0)

    def get_angle(self):
        return {
            "UP": 0,
            "RIGHT": -90,
            "LEFT": 90,
            "DOWN": 180,
        }.get(self.name)

    def rotate_right(self):
        return {
            "UP": self.RIGHT,
            "RIGHT": self.DOWN,
            "DOWN": self.LEFT,
            "LEFT": self.UP,
        }.get(self.name)

    def rotate_left(self):
        return {
            "RIGHT": self.UP,
            "DOWN": self.RIGHT,
            "LEFT": self.DOWN,
            "UP": self.LEFT,
        }.get(self.name)


class Movable(GameObject):

    def __init__(self, *args, **kwargs):
        super(Movable, self).__init__(*args, **kwargs)
        self.sprite = None
        self.speed = 0
        self.direction = Directions.UP

    def move(self, direction: Directions) -> pygame.rect.Rect:
        if self.direction != direction:
            angle = direction.get_angle()
            self.image = pygame.transform.rotate(self.sprite, angle)
            self.direction = direction
        step = direction.value * self.speed
        return self.rect.move(*step)
