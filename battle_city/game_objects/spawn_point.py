import random
from typing import List

import pygame

from battle_city.game_objects import GameObject
from battle_city.utils import Vector


class SpawnPoint:

    def __init__(self, classes: List[GameObject], count: int, key: str):
        for cls in classes:
            assert issubclass(cls, GameObject),\
                f"{cls} should derived from GameObject"

        self.classes = classes
        self.count = count
        self.key = key
        self.is_empty = False

    def __call__(self, position: Vector, *groups):
        self.position = position
        return self

    def update(self, event: pygame.event, level):
        print(self.position)
        if self.count == 0:
            self.is_empty = True
        self.count -= 1
        cls = random.choice(self.classes)
        level[self.key].add(cls(self.position))
