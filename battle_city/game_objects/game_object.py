import pygame
from typing import Tuple
from enum import Enum


class GameObject:

    def __init__(self, position: Tuple[float, float]):
        self.position = position
        self.image = None

    def draw(self, screen: pygame.display) -> None:

        if self.image and self.position:
            screen.blit(self.image, self.position)

    def is_collided_with(self, obj: pygame.rect) -> bool:
        return self.image.get_rect().colliderect(obj)

    def on_event(self, event: pygame.event, level):
        pass


class Directions(Enum):
    UP = (0, 1)
    RIGHT = (1, 0)
    DOWN = (0, -1)
    LEFT = (-1, 0)

    def next(self):
        return {
            "UP": self.RIGHT,
            "RIGHT": self.DOWN,
            "DOWN": self.LEFT,
            "LEFT": self.UP,
        }.get(self.name)

    def previous(self):
        return {
            "RIGHT": self.UP,
            "DOWN": self.RIGHT,
            "LEFT": self.DOWN,
            "UP": self.LEFT,
        }.get(self.name)
