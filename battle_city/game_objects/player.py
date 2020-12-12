from typing import Tuple

import pygame

from battle_city.config import CELL_SIZE
from battle_city.game_objects import Tank
from battle_city.game_objects import Directions


class Player(Tank):

    def __init__(self, position, *args, **kwars):
        super().__init__(position, *args, **kwars)
        self.sprite = pygame.image.load("battle_city/media/images/player.png")
        self.sprite = pygame.transform.scale(self.sprite, CELL_SIZE)
        self.image = pygame.transform.rotate(self.sprite, 0)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position.x, position.y
        self.direction = Directions.UP
        self.speed = 5

    def update(self, event: pygame.event, level, *args):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                new_position = self.move(Directions.RIGHT)
                self.rect = self.set_position(new_position, level)
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                new_position = self.move(Directions.LEFT)
                self.rect = self.set_position(new_position, level)
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                new_position = self.move(Directions.UP)
                self.rect = self.set_position(new_position, level)
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                new_position = self.move(Directions.DOWN)
                self.rect = self.set_position(new_position, level)
            if event.key == pygame.K_SPACE:
                self.shot(level)
