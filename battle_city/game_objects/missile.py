import pygame

from battle_city.config import CELL_SIZE
from battle_city.game_objects.game_object import Directions, Movable

import logging

logger = logging.getLogger(__name__)


class Missile(Movable):
    image = "battle_city/media/images/missile.png"

    def __init__(self, direction: Directions, position, *args, **kwargs):
        super().__init__(position, *args, **kwargs)
        self.image = pygame.image.load("battle_city/media/images/missile.png")
        self.image = pygame.transform.scale(self.image, CELL_SIZE)
        self.image = pygame.transform.rotate(self.image, direction.get_angle())

        self.direction = direction
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position.x, position.y
        self.speed = 5 * 3

        logger.debug(f"Missle was created on position: \
        {position} with direction {self.direction}")

    def update(self, event: pygame.event, level, *args):
        new_position = self.move(self.direction)
        wall_index = new_position.collidelist(level['W'].sprites())
        iron_index = new_position.collidelist(level['I'].sprites())
        player_index = new_position.collidelist(level['P'].sprites())
        tank_index = new_position.collidelist(level['T'].sprites())
        if player_index >= 0:
            level['P'].sprites()[player_index].kill()
            self.kill()
        if tank_index >= 0:
            level['T'].sprites()[tank_index].kill()
            self.kill()
        if wall_index >= 0:
            level['W'].sprites()[wall_index].kill()
            self.kill()
        elif not self.in_borders(new_position, level) or iron_index != -1:
            self.kill()
        else:
            self.rect = new_position
