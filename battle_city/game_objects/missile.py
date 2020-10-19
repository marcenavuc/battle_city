from typing import Tuple

import pygame

from battle_city.game_objects import Wall
from battle_city.game_objects.game_object import GameObject, Directions


class Missile(GameObject):
    trans_to_angle = {
        Directions.UP: 0,
        Directions.LEFT: 90,
        Directions.DOWN: 180,
        Directions.RIGHT: 270,
    }

    def __init__(self, direction: Directions, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = pygame.image.load("battle_city/media/images/missile.png")
        self.image = pygame.transform.rotate(self.image,
                                             self.trans_to_angle[direction])
        self.direction = direction

    def on_event(self, event: pygame.event, level):
        pygame.time.delay(5)
        new_position = self.go_forward()
        if self.can_fly(new_position, level):
            self.position = new_position
        elif level[new_position].__class__ != GameObject:
            level[new_position] = GameObject(new_position)
            level[self.position] = GameObject(self.position)
        else:
            level[self.position] = GameObject(self.position)

    def go_forward(self) -> Tuple[int, int]:
        return (self.position[0] + self.direction.value[0],
                self.position[1] - self.direction.value[1])

    def can_fly(self, position: Tuple[int, int], level) -> bool:
        return not isinstance(level[position], Wall) \
                and 0 < position[0] <= level.max_x \
                and 0 < position[1] <= level.max_y
