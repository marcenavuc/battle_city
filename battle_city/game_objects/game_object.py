import pygame
from enum import Enum

from battle_city.utils import Vector


class GameObject:

    def __init__(self, position: Vector):
        self.position = position
        self.image = None

    def draw(self, screen: pygame.display) -> None:
        if self.image and self.position:
            screen.blit(self.image, self.position)

    def is_collided_with(self, obj: pygame.rect) -> bool:
        return self.image.get_rect().colliderect(obj)

    def on_event(self, event: pygame.event, level):
        pass

    @staticmethod
    def in_borders(position: Vector, level) -> bool:
        return 0 <= position[0] <= level.max_x \
               and 0 <= position[1] <= level.max_y


class Empty(GameObject):
    pass


class Directions(Enum):
    UP = Vector(0, 1)
    RIGHT = Vector(1, 0)
    DOWN = Vector(0, -1)
    LEFT = Vector(-1, 0)

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
