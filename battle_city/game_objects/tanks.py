import logging
import random
import time

import pygame

from battle_city.config import RESPAWN_TIME
from battle_city.game_objects import Missile
from battle_city.game_objects.game_object import Directions, Movable

logger = logging.getLogger(__name__)


class Tank(Movable):
    image = "battle_city/media/images/tank.png"

    def __init__(self, position, *args, **kwars):
        super().__init__(position, *args, **kwars)
        self.health = 1
        self.speed = 5
        self.is_shot = True
        self.period_duration = RESPAWN_TIME / 8
        self.time_of_creation = time.time()

    def set_position(self, position: pygame.rect.Rect, level) \
            -> pygame.rect.Rect:
        if (
            self.in_borders(position, level)
            and position.collidelist(level["WALL"].sprites()) < 0
            and position.collidelist(level["AQUA"].sprites()) < 0
            and position.collidelist(level["IRON"].sprites()) < 0
        ):
            return position
        return self.rect

    def shot(self, level):
        self.speed, speed = 13 * 3, self.speed
        missile_position = self.move(self.direction)
        self.speed = speed
        if self.is_shot and missile_position != self.rect:
            missile = Missile(missile_position, self.direction)
            level.groups["MISSILE"].add(missile)


class EnemyTank(Tank):
    image = "battle_city/media/images/tank.png"

    def __init__(self, position, *args, **kwars):
        super().__init__(position, *args, **kwars)

    def update(self, event: pygame.event, level, *args):
        if abs(self.time_of_creation - time.time()) < self.period_duration:
            self.random_walk(level)
        elif abs(self.time_of_creation - time.time()) < 2*self.period_duration:
            self.move_to_obj("PLAYER", level)
        else:
            self.move_to_obj("BASE", level)

    def random_walk(self, level):
        rand_number = random.randint(1, 1000)
        direction = self.direction
        if rand_number < 100:
            direction = Directions.random_direction()
        if rand_number < 50:
            self.shot(level)

        new_position = self.move(direction)
        self.rect = self.set_position(new_position, level)

    def move_to_obj(self, key: str, level):
        obj = level[key].sprites()[0]
        direction = self.direction
        if self.rect.y + self.speed < obj.rect.y:
            direction = Directions.DOWN
        elif self.rect.y - self.speed > obj.rect.y:
            direction = Directions.UP
        elif self.rect.x - self.speed < obj.rect.x:
            direction = Directions.RIGHT
        elif self.rect.x + self.speed > obj.rect.x:
            direction = Directions.LEFT

        new_position = self.move(direction)
        new_rect = self.set_position(new_position, level)
        if self.rect == new_rect:
            logger.debug("Didn't found the way")
            self.period_duration *= 2
        else:
            self.rect = new_rect


class SpeedTank(EnemyTank):
    image = "battle_city/media/images/tank.png"

    def __init__(self, position, *args, **kwars):
        super().__init__(position, *args, **kwars)
        self.speed = 10


class HeavyTank(EnemyTank):
    image = "battle_city/media/images/heavy_tank.png"

    def __init__(self, position, *args, **kwars):
        super().__init__(position, *args, **kwars)
        self.speed = 2
        self.health = 3


class RushTank(EnemyTank):
    image = "battle_city/media/images/rush_tank.png"

    def __init__(self, position, *args, **kwars):
        super().__init__(position, *args, **kwars)
        self.speed = 5

    def update(self, event: pygame.event, level, *args):
        self.move_to_obj("B", level)