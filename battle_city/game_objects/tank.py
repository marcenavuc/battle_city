from typing import Tuple

import pygame

from battle_city.config import CELL_WIDTH, CELL_HEIGHT
from battle_city.game_objects.game_object import GameObject, Directions


class Tank(GameObject):

    def __init__(self, *args, **kwars):
        super().__init__(*args, **kwars)
        self.image = pygame.image.load("battle_city/media/images/enemy.png")
        self.direction = Directions.DOWN

    def on_event(self, event: pygame.event, level):
        pass

    def go_right(self):
        self.image = pygame.transform.rotate(self.image, 270)
        self.direction = self.direction.next()

    def go_left(self):
        self.image = pygame.transform.rotate(self.image, 90)
        self.direction = self.direction.previous()

    def go_forward(self) -> Tuple[int, int]:
        return (self.position[0] + self.direction.value[0],
                self.position[1] - self.direction.value[1])

    def go_back(self) -> Tuple[int, int]:
        return (self.position[0] - self.direction.value[0],
                self.position[1] + self.direction.value[1])
