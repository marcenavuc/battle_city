import time

import pygame

from battle_city.config import CELL_SIZE
from battle_city.utils import Vector
from battle_city.game_objects import Wall, Missile
from battle_city.game_objects.game_object import Directions, Movable


class Tank(Movable):

    def __init__(self, position, *args, **kwars):
        super().__init__(position, *args, **kwars)
        self.sprite = pygame.image.load("battle_city/media/images/enemy.png")
        self.sprite = pygame.transform.scale(self.sprite, CELL_SIZE)
        self.image = pygame.transform.rotate(self.sprite, 0)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position.x, position.y
        self.direction = Directions.DOWN

        self.is_shot = True
        self.speed = 5

    def on_event(self, event: pygame.event, level):
        # if self.is_shot:
        #     self.shot(level)
        self.is_shot = False

    def set_position(self, position: pygame.rect.Rect, level) -> pygame.rect.Rect:
        if self.in_borders(position, level) and \
                position.collidelist(level['W'].sprites()) < 0 and \
                position.collidelist(level['A'].sprites()) < 0 and \
                position.collidelist(level['I'].sprites()):
            return position
        return self.rect

    def shot(self, level):
        missile_position = self.set_position(self.move(self.direction), level)
        if self.is_shot and missile_position != self.rect:
            level.groups["M"].add(Missile(self.direction, missile_position))
            # level[missile_position] = Missile(self.direction, missile_position)
