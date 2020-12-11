from typing import Tuple

import pygame

from battle_city.game_objects import Tank
from battle_city.game_objects import Directions


class Player(Tank):

    def __init__(self, *args, **kwars):
        super().__init__(*args, **kwars)
        self.image = pygame.image.load("battle_city/media/images/player.png")
        self.direction = Directions.UP

    def on_event(self, event: pygame.event, level):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                # self.go_right()
                new_position = self.move(Directions.RIGHT)
                self.position = self.set_position(new_position, level)
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                # self.go_left()
                new_position = self.move(Directions.LEFT)
                self.position = self.set_position(new_position, level)
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                # new_position = self.go_forward()
                new_position = self.move(Directions.DOWN)
                self.position = self.set_position(new_position, level)
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                # new_position = self.go_back()
                new_position = self.move(Directions.UP)
                self.position = self.set_position(new_position, level)
            if event.key == pygame.K_SPACE:
                self.shot(level)
