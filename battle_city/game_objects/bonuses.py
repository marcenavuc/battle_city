import random

import pygame

from battle_city.game_objects import GameObject


class Bonus(GameObject):
    image = "battle_city/media/images/bonus_hat.png"

    def __init__(self, position, *args, **kwars):
        super().__init__(position, *args)

    def update(self, event: pygame.event, level, *args):
        player_index = self.rect.collidelist(level["PLAYER"].sprites())
        if player_index != -1:
            player = level["PLAYER"].sprites()[player_index]
            self.modify_player(player, level)
            self.kill()

    def modify_player(self, player, level):
        pass


class HealthBonus(Bonus):
    image = "battle_city/media/images/bonus_hat.png"

    def modify_player(self, player, level):
        player.health += 1


class SpeedBonus(Bonus):
    image = "battle_city/media/images/bonus_showel.png"

    def modify_player(self, player, level):
        player.speed *= 2


class RandomKill(Bonus):
    image = "battle_city/media/images/bonus_tank.png"

    def modify_player(self, player, level):
        for tank in level["TANKS"]:
            if random.randint(0, 1):
                tank.kill()
