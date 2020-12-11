from typing import Tuple

import pygame

from battle_city.game_objects import Tank
from battle_city.game_objects import Directions


class Player(Tank):

    def __init__(self, *args, **kwars):
        super().__init__(*args, **kwars)
        self.sprite = pygame.image.load("battle_city/media/images/player.png")
        self.direction = Directions.UP
        self.image = pygame.transform.rotate(self.sprite, 0)

    def on_event(self, event: pygame.event, level):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                new_position = self.move(Directions.RIGHT)
                self.position = self.set_position(new_position, level)
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                new_position = self.move(Directions.LEFT)
                self.position = self.set_position(new_position, level)
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                new_position = self.move(Directions.UP)
                self.position = self.set_position(new_position, level)
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                new_position = self.move(Directions.DOWN)
                self.position = self.set_position(new_position, level)
            if event.key == pygame.K_SPACE:
                self.shot(level)
