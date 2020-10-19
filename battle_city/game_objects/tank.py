from typing import Tuple

import pygame

from battle_city.game_objects import Wall, Missile
from battle_city.game_objects.game_object import GameObject, Directions


class Tank(GameObject):

    def __init__(self, *args, **kwars):
        super().__init__(*args, **kwars)
        self.image = pygame.image.load("battle_city/media/images/enemy.png")
        self.direction = Directions.DOWN

    def on_event(self, event: pygame.event, level):
        self.shot(level)

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

    def set_position(self, position: Tuple[int, int], level) \
            -> Tuple[int, int]:
        if not isinstance(level[position], Wall) \
                and 0 <= position[0] <= level.max_x \
                and 0 <= position[1] <= level.max_y:
            return position
        return self.position

    def shot(self, level):
        missile_position = self.go_forward()
        level[missile_position] = Missile(self.direction, missile_position)
