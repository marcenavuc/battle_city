import logging

import pygame

from battle_city.game_objects.game_object import Directions, Movable

logger = logging.getLogger(__name__)


class Missile(Movable):
    image = "media/images/missile.png"

    def __init__(self, position, direction: Directions, *args, **kwargs):
        super().__init__(position, *args, **kwargs)
        self.direction = direction
        self.image = pygame.transform.rotate(self.sprite, direction.get_angle())
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position.x, position.y
        self.speed = 15
        logger.debug(
            f"Missle was created on position: \
        {position} with direction {self.direction}"
        )

    def update(self, event: pygame.event, level, *args):
        position = self.move(self.direction)
        tank_index = self.is_collidelist(position, level.tanks)
        wall_index = self.is_collidelist(position, level.walls)
        if position.colliderect(level.command_center.rect):
            level.command_center = None
            self.kill(level)
        elif position.colliderect(level.player.rect):
            if level.player.health > 0:
                level.player.health -= 1
            else:
                logger.debug("Player killed")
                level.player = None
            self.kill(level)
        elif tank_index >= 0:
            tank = level.tanks[tank_index]
            if tank.health > 0:
                tank.health -= 1
            else:
                level.tanks.remove(tank)
            self.kill(level)
        elif wall_index >= 0:
            logger.debug(f"Hitted in wall {wall_index}")
            wall = level.walls[wall_index]
            if wall.health > 0:
                wall.health -= 1
            else:
                logger.debug(f"Killing wall {wall_index}")
                level.walls.remove(wall)
            self.kill(level)
        elif not self.in_borders(position, level) \
                or self.is_collidelist(position, level.blocks) >= 0:
            self.kill(level)
        else:
            self.rect = position

    def kill(self, level):
        level.missiles.remove(self)
