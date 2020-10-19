import pygame

from battle_city.game_objects.game_object import GameObject


class Wall(GameObject):

    def __init__(self, *args, **kwars):
        super().__init__(*args, **kwars)
        self.image = pygame.image.load("battle_city/media/images/wall.png")
