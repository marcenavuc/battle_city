import pygame

from battle_city.game_objects.game_object import Directions, Movable

import logging

logger = logging.getLogger(__name__)


class Missile(Movable):
    image = "battle_city/media/images/missile.png"

    def __init__(self, position, direction: Directions, *args, **kwargs):
        super().__init__(position, *args, **kwargs)
        self.direction = direction
        self.image = pygame.transform.rotate(self.image, direction.get_angle())
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position.x, position.y
        self.speed = 15

        logger.debug(f"Missle was created on position: \
        {position} with direction {self.direction}")

    def update(self, event: pygame.event, level, *args):
        new_position = self.move(self.direction)
        wall_index = new_position.collidelist(level['WALL'].sprites())
        iron_index = new_position.collidelist(level['IRON'].sprites())
        player_index = new_position.collidelist(level['PLAYER'].sprites())
        tank_index = new_position.collidelist(level['TANK'].sprites())
        if player_index >= 0:
            level['PLAYER'].sprites()[player_index].kill()
            self.kill()
        if tank_index >= 0:
            level['TANK'].sprites()[tank_index].kill()
            self.kill()
        if wall_index >= 0:
            level['WALL'].sprites()[wall_index].kill()
            self.kill()
        elif not self.in_borders(new_position, level) or iron_index != -1:
            self.kill()
        else:
            self.rect = new_position
