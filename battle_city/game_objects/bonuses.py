import random

import pygame

from battle_city.game_objects import GameObject


class Bonus(GameObject):
    image = "media/images/bonus_hat.png"

    def __init__(self, position, *args, **kwargs):
        super().__init__(position, *args, **kwargs)

    def update(self, event: pygame.event, level, *args):
        if self.is_collide(self, level.player):
            self.modify_player(level.player, level)
            level.bonuses.remove(self)

    def modify_player(self, player, level):
        pass


class LifeBonus(Bonus):
    image = "media/images/bonus_hat.png"

    def modify_player(self, player, level):
        player.health += 1


class SpeedBonus(Bonus):
    image = "media/images/bonus_showel.png"

    def modify_player(self, player, level):
        player.speed *= 2


class RandomKillBonus(Bonus):
    image = "media/images/bonus_tank.png"

    def modify_player(self, player, level):
        for tank in level.tanks:
            if random.randint(0, 1):
                level.tanks.remove(tank)
