import pygame

from battle_city.config import CELL_SIZE
from battle_city.utils import Vector
from battle_city.game_objects import Wall
from battle_city.game_objects.game_object import GameObject, Directions, Movable

import logging

logger = logging.getLogger(__name__)


class Missile(Movable):

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
        # new_position = self.go_forward()
        # if self.can_fly(new_position, level):
        #     self.position = new_position
        # elif level[new_position].__class__ != GameObject:  # Врезались во что-то
        #     level.remove(self.position)
        #     level.remove(new_position)
        # else:
        #     level.remove(self.position)
        new_position = self.move(self.direction)
        wall_index = new_position.collidelist(level['W'].sprites())
        iron_index = new_position.collidelist(level['I'].sprites())
        if wall_index >= 0:
            level['W'].remove(level['W'].sprites()[wall_index])
            level['M'].remove(self)
        elif not self.in_borders(new_position, level) or iron_index != -1:
            level['M'].remove(self)
        else:
            self.rect = new_position

        # if self.set_position(new_position, level) != new_position:
        #     print(new_position)
        #     self.rect = new_position
        # else:
        #     level['M'].remove(self)
